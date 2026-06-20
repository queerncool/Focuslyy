import { useEffect } from 'react';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { useBrandFonts } from '@/theme';
import { useProfileStore } from '@/state';

SplashScreen.preventAutoHideAsync().catch(() => {
  /* no-op: splash may already be hidden */
});

export default function RootLayout() {
  const [fontsLoaded, fontError] = useBrandFonts();
  const ensureAnonymousId = useProfileStore((s) => s.ensureAnonymousId);

  // Anonymous-default identity (§B.5): every install gets a stable UUID on
  // first launch, which later aliases to a real account on sign-in.
  useEffect(() => {
    ensureAnonymousId();
  }, [ensureAnonymousId]);

  useEffect(() => {
    if (fontsLoaded || fontError) {
      SplashScreen.hideAsync().catch(() => {});
    }
  }, [fontsLoaded, fontError]);

  // Hold the splash until brand fonts are ready (or fail) so we never flash
  // system fonts in place of the locked typefaces.
  if (!fontsLoaded && !fontError) {
    return null;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <StatusBar style="light" />
        <Stack screenOptions={{ headerShown: false }}>
          <Stack.Screen name="(app)" />
          <Stack.Screen name="(onboarding)" />
          <Stack.Screen
            name="(session)"
            options={{ presentation: 'modal' }}
          />
          <Stack.Screen name="invite" options={{ presentation: 'modal' }} />
          <Stack.Screen name="saveAccount" options={{ presentation: 'modal' }} />
        </Stack>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
