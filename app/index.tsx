import { useEffect, useState } from 'react';
import { Redirect } from 'expo-router';
import { useProfileStore } from '@/state';

/**
 * Entry gate. Brand-new users go through the onboarding funnel; returning
 * users land on the main tabs. We wait for the persisted profile to hydrate
 * so we don't flash the funnel at someone who already finished it.
 */
export default function Index() {
  const hasOnboarded = useProfileStore((s) => s.hasOnboarded);
  const [hydrated, setHydrated] = useState(() =>
    useProfileStore.persist.hasHydrated()
  );

  useEffect(() => {
    const unsub = useProfileStore.persist.onFinishHydration(() =>
      setHydrated(true)
    );
    setHydrated(useProfileStore.persist.hasHydrated());
    return unsub;
  }, []);

  if (!hydrated) return null;

  return <Redirect href={hasOnboarded ? '/focus' : '/start'} />;
}
