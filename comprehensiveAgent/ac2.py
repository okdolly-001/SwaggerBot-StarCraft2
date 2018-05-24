import collections
import os
import numpy as np
import tensorflow as tf
from pysc2.lib import actions
from tensorflow.contrib import layers
from tensorflow.contrib.layers.python.layers.optimizers import OPTIMIZER_SUMMARIES
from actorcritic.policy import FullyConvPolicy
from common.preprocess import ObsProcesser, FEATURE_KEYS, AgentInputTuple
from common.util import weighted_random_sample, select_from_each_row, ravel_index_pairs


    def build_model(self):
        self.placeholders = _get_placeholders(self.spatial_dim)

        with tf.variable_scope("theta"):
            theta = self.policy(self, trainable=True).build()

        selected_spatial_action_flat = ravel_index_pairs(
            self.placeholders.selected_spatial_action, self.spatial_dim
        )

        selected_log_probs = self._get_select_action_probs(theta, selected_spatial_action_flat)

        # maximum is to avoid 0 / 0 because this is used to calculate some means
        sum_spatial_action_available = tf.maximum(
            1e-10, tf.reduce_sum(self.placeholders.is_spatial_action_available)
        )

        neg_entropy_spatial = tf.reduce_sum(
            theta.spatial_action_probs * theta.spatial_action_log_probs
        ) / sum_spatial_action_available
        neg_entropy_action_id = tf.reduce_mean(tf.reduce_sum(
            theta.action_id_probs * theta.action_id_log_probs, axis=1
        ))

        if self.mode == ACMode.PPO:
            # could also use stop_gradient and forget about the trainable
            with tf.variable_scope("theta_old"):
                theta_old = self.policy(self, trainable=False).build()

            new_theta_var = tf.global_variables("theta/")
            old_theta_var = tf.global_variables("theta_old/")

            assert len(tf.trainable_variables("theta/")) == len(new_theta_var)
            assert not tf.trainable_variables("theta_old/")
            assert len(old_theta_var) == len(new_theta_var)

            self.update_theta_op = [
                tf.assign(t_old, t_new) for t_new, t_old in zip(new_theta_var, old_theta_var)
            ]

            selected_log_probs_old = self._get_select_action_probs(
                theta_old, selected_spatial_action_flat
            )
            ratio = tf.exp(selected_log_probs.total - selected_log_probs_old.total)
            clipped_ratio = tf.clip_by_value(
                ratio, 1.0 - self.clip_epsilon, 1.0 + self.clip_epsilon
            )
            l_clip = tf.minimum(
                ratio * self.placeholders.advantage,
                clipped_ratio * self.placeholders.advantage
            )
            self.sampled_action_id = weighted_random_sample(theta_old.action_id_probs)
            self.sampled_spatial_action = weighted_random_sample(theta_old.spatial_action_probs)
            self.value_estimate = theta_old.value_estimate
            self._scalar_summary("action/ratio", tf.reduce_mean(clipped_ratio))
            self._scalar_summary("action/ratio_is_clipped",
                tf.reduce_mean(tf.to_float(tf.equal(ratio, clipped_ratio))))
            policy_loss = -tf.reduce_mean(l_clip)
        else:
            self.sampled_action_id = weighted_random_sample(theta.action_id_probs)
            self.sampled_spatial_action = weighted_random_sample(theta.spatial_action_probs)
            self.value_estimate = theta.value_estimate
            policy_loss = -tf.reduce_mean(selected_log_probs.total * self.placeholders.advantage)

        value_loss = tf.losses.mean_squared_error(
            self.placeholders.value_target, theta.value_estimate)

        loss = (
            policy_loss
            + value_loss * self.loss_value_weight
            + neg_entropy_spatial * self.entropy_weight_spatial
            + neg_entropy_action_id * self.entropy_weight_action_id
        )

        self.train_op = layers.optimize_loss(
            loss=loss,
            global_step=tf.train.get_global_step(),
            optimizer=self.optimiser,
            clip_gradients=self.max_gradient_norm,
            summaries=OPTIMIZER_SUMMARIES,
            learning_rate=None,
            name="train_op"
        )

        self._scalar_summary("value/estimate", tf.reduce_mean(self.value_estimate))
        self._scalar_summary("value/target", tf.reduce_mean(self.placeholders.value_target))
        self._scalar_summary("action/is_spatial_action_available",
            tf.reduce_mean(self.placeholders.is_spatial_action_available))
        self._scalar_summary("action/selected_id_log_prob",
            tf.reduce_mean(selected_log_probs.action_id))
        self._scalar_summary("loss/policy", policy_loss)
        self._scalar_summary("loss/value", value_loss)
        self._scalar_summary("loss/neg_entropy_spatial", neg_entropy_spatial)
        self._scalar_summary("loss/neg_entropy_action_id", neg_entropy_action_id)
        self._scalar_summary("loss/total", loss)
        self._scalar_summary("value/advantage", tf.reduce_mean(self.placeholders.advantage))
        self._scalar_summary("action/selected_total_log_prob",
            tf.reduce_mean(selected_log_probs.total))
        self._scalar_summary("action/selected_spatial_log_prob",
            tf.reduce_sum(selected_log_probs.spatial) / sum_spatial_action_available)

        self.init_op = tf.global_variables_initializer()
        self.saver = tf.train.Saver(max_to_keep=2)
        self.all_summary_op = tf.summary.merge_all(tf.GraphKeys.SUMMARIES)
        self.scalar_summary_op = tf.summary.merge(tf.get_collection(self._scalar_summary_key))

    def _input_to_feed_dict(self, input_dict):
        return {k + ":0": v for k, v in input_dict.items()}

    def step(self, obs):
        feed_dict = self._input_to_feed_dict(obs)

        action_id, spatial_action, value_estimate = self.sess.run(
            [self.sampled_action_id, self.sampled_spatial_action, self.value_estimate],
            feed_dict=feed_dict
        )

        spatial_action_2d = np.array(
            np.unravel_index(spatial_action, (self.spatial_dim,) * 2)
        ).transpose()

        return action_id, spatial_action_2d, value_estimate

    def train(self, input_dict):
        feed_dict = self._input_to_feed_dict(input_dict)
        ops = [self.train_op]

        write_all_summaries = (
            (self.train_step % self.all_summary_freq == 0) and
            self.summary_path is not None
        )
        write_scalar_summaries = (
            (self.train_step % self.scalar_summary_freq == 0) and
            self.summary_path is not None
        )

        if write_all_summaries:
            ops.append(self.all_summary_op)
        elif write_scalar_summaries:
            ops.append(self.scalar_summary_op)

        r = self.sess.run(ops, feed_dict)

        if write_all_summaries or write_scalar_summaries:
            self.summary_writer.add_summary(r[-1], global_step=self.train_step)

        self.train_step += 1

    def get_value(self, obs):
        feed_dict = self._input_to_feed_dict(obs)
        return self.sess.run(self.value_estimate, feed_dict=feed_dict)

    def flush_summaries(self):
        self.summary_writer.flush()

    def save(self, path, step=None):
        os.makedirs(path, exist_ok=True)
        step = step or self.train_step
        print("saving model to %s, step %d" % (path, step))
        self.saver.save(self.sess, path + '/model.ckpt', global_step=step)

    def load(self, path):
        ckpt = tf.train.get_checkpoint_state(path)
        self.saver.restore(self.sess, ckpt.model_checkpoint_path)
        self.train_step = int(ckpt.model_checkpoint_path.split('-')[-1])
        print("loaded old model with train_step %d" % self.train_step)
        self.train_step += 1

    def update_theta(self):
        if self.mode == ACMode.PPO:
            self.sess.run(self.update_theta_op)
