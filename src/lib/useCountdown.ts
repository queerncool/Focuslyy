import { useEffect, useRef, useState } from 'react';

/**
 * Wall-clock countdown. Drives Ritual (0:30), Locked (blockMin), and Break
 * (5:00). Anchored to an end timestamp so it stays accurate across ticks and
 * doesn't drift if the JS thread stutters. Fires `onComplete` once at zero.
 */
export function useCountdown(durationSec: number, onComplete?: () => void) {
  const [remaining, setRemaining] = useState(durationSec);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  useEffect(() => {
    const end = Date.now() + durationSec * 1000;
    let done = false;
    setRemaining(durationSec);

    const tick = () => {
      const rem = Math.max(0, Math.round((end - Date.now()) / 1000));
      setRemaining(rem);
      if (rem <= 0 && !done) {
        done = true;
        clearInterval(id);
        onCompleteRef.current?.();
      }
    };

    const id = setInterval(tick, 250);
    return () => clearInterval(id);
  }, [durationSec]);

  return remaining;
}
