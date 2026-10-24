import type { VideoSource } from 'expo-video';

/**
 * "Watch the demo" video (Start screen → /demo).
 *
 * This should be the App Preview recording from docs/STORE.md §3: one full
 * session, Set Session → Seal → Locked → Break → Log Win → Share, no audio.
 * Either a hosted .mp4 URL (swap the video without an app update) or a bundled
 * file, e.g. `require('../../assets/video/demo.mp4')`.
 *
 * Until a real video is set here the "Watch the demo" button stays hidden, so
 * it can never ship as a dead-end CTA.
 */
export const DEMO_VIDEO: VideoSource = null;

export const hasDemoVideo = DEMO_VIDEO != null;
