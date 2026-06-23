import { useEffect, useState } from 'react';
import { router } from 'expo-router';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  Pill,
  Screen,
} from '@/components';
import { recommendedApps, SEAL_APPS } from '@/lib/session';
import { haptic } from '@/lib/haptics';
import { useQuizStore, useSessionStore } from '@/state';
import { border, colors, fontFamily, radius, spacing } from '@/theme';

export default function SealApps() {
  const distractions = useQuizStore((s) => s.distractions);
  const storedApps = useSessionStore((s) => s.blockedApps);
  const setBlockedApps = useSessionStore((s) => s.setBlockedApps);

  const recommended = recommendedApps(distractions);

  // Seed selection: keep an existing one, else pre-check the Q2 recommendations.
  const [selected, setSelected] = useState<string[]>(
    storedApps.length > 0 ? storedApps : recommended
  );

  // Keep the store in sync so the count carries through to Locked.
  useEffect(() => {
    setBlockedApps(selected);
  }, [selected, setBlockedApps]);

  const toggle = (app: string) => {
    haptic.light();
    setSelected((prev) =>
      prev.includes(app) ? prev.filter((a) => a !== app) : [...prev, app]
    );
  };

  return (
    <Screen style={styles.screen}>
      <View style={styles.header}>
        <KickerLabel>Seal apps</KickerLabel>
        <Display style={styles.headline}>Block what pulls you out.</Display>
        <View style={styles.countRow}>
          <Pill
            label={`${selected.length} sealed`}
            tone={selected.length > 0 ? 'amber' : 'muted'}
          />
        </View>
      </View>

      <ScrollView
        style={styles.flex}
        contentContainerStyle={styles.list}
        showsVerticalScrollIndicator={false}
      >
        {SEAL_APPS.map((app) => {
          const on = selected.includes(app);
          const forYou = recommended.includes(app);
          return (
            <Pressable
              key={app}
              accessibilityRole="switch"
              accessibilityState={{ checked: on }}
              accessibilityHint={`Toggle sealing ${app}`}
              onPress={() => toggle(app)}
              style={[styles.row, on && styles.rowOn]}
            >
              <View style={styles.rowLeft}>
                <Text style={styles.appName}>{app}</Text>
                {forYou && <Pill label="For you" tone="amber" style={styles.forYou} />}
              </View>
              <View style={[styles.check, on && styles.checkOn]}>
                {on && <Text style={styles.checkMark}>✓</Text>}
              </View>
            </Pressable>
          );
        })}

        <Body style={styles.note}>
          Real OS-level blocking arrives with the iOS update. For now the seal
          runs on your honor — same ritual, same streak.
        </Body>
      </ScrollView>

      <View style={styles.footer}>
        <Button
          label="Seal & start ritual →"
          disabled={selected.length === 0}
          onPress={() => router.push('/ritual')}
          accessibilityHint="Lock these apps and begin the focus ritual"
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  flex: {
    flex: 1,
  },
  header: {
    paddingTop: spacing.lg,
  },
  headline: {
    marginTop: spacing.base,
  },
  countRow: {
    flexDirection: 'row',
    marginTop: spacing.base,
  },
  list: {
    paddingTop: spacing.lg,
    paddingBottom: spacing.lg,
    gap: spacing.sm,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: 56,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: border.subtle,
    backgroundColor: colors.ink,
  },
  rowOn: {
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.12)',
  },
  rowLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    flexShrink: 1,
  },
  appName: {
    fontFamily: fontFamily.display,
    fontSize: 17,
    color: colors.cream,
  },
  forYou: {
    paddingVertical: 2,
  },
  check: {
    width: 28,
    height: 28,
    borderRadius: radius.sm,
    borderWidth: 1.5,
    borderColor: colors.muted,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkOn: {
    borderColor: colors.amber,
    backgroundColor: colors.amber,
  },
  checkMark: {
    fontFamily: fontFamily.monoBold,
    fontSize: 16,
    color: colors.espresso,
  },
  note: {
    marginTop: spacing.base,
    fontSize: 13,
    lineHeight: 19,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
});
