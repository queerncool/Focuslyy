import { useRef, useState } from 'react';
import { router, useLocalSearchParams } from 'expo-router';
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { Button, Display, KickerLabel, Screen } from '@/components';
import { chipsForMode, SESSION_XP } from '@/lib/session';
import { formatDuration } from '@/lib/time';
import {
  useProfileStore,
  useQuizStore,
  useSessionStore,
  useSessionsHistoryStore,
} from '@/state';
import type { Session } from '@/types';
import { colors, fontFamily, radius, spacing } from '@/theme';

function makeId() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

export default function LogWin() {
  const { broke } = useLocalSearchParams<{ broke?: string }>();
  const sealBroken = broke === '1';

  const mode = useQuizStore((s) => s.mode);
  const streakDays = useProfileStore((s) => s.streakDays);

  const task = useSessionStore((s) => s.task);
  const blockMin = useSessionStore((s) => s.blockMin);
  const blockedApps = useSessionStore((s) => s.blockedApps);
  const startedAt = useSessionStore((s) => s.startedAt);
  const addSession = useSessionsHistoryStore((s) => s.addSession);

  const [note, setNote] = useState('');
  const savedRef = useRef(false);

  // Completed blocks count full length; a broken seal counts the time served.
  const elapsedMin =
    startedAt != null
      ? Math.max(0, Math.round((Date.now() - startedAt) / 60000))
      : 0;
  const durationMin = sealBroken ? Math.min(elapsedMin, blockMin) : blockMin;

  // They just worked today, so the streak is at least 1. Real streak math
  // (consecutive days from history) lands with Stats in Phase 4.
  const streak = Math.max(streakDays, 1);
  const taskLabel = task.trim();
  const chips = chipsForMode(mode);

  const save = () => {
    if (savedRef.current) return;
    savedRef.current = true;

    const session: Session = {
      id: makeId(),
      startedAt: startedAt ?? Date.now(),
      endedAt: Date.now(),
      durationMin,
      mode,
      task: taskLabel,
      note: note.trim(),
      completed: !sealBroken,
      blockedApps,
    };
    addSession(session);
    router.replace('/share');
  };

  return (
    <Screen style={styles.screen}>
      <ScrollView
        style={styles.flex}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        <KickerLabel color={sealBroken ? colors.muted : colors.amber}>
          {sealBroken ? 'Seal broken' : 'Session complete'}
        </KickerLabel>
        <Display style={styles.headline}>
          {sealBroken ? "You stepped out — that's okay." : 'You locked in.'}
        </Display>

        <View style={styles.stats}>
          <Stat label="TIME" value={formatDuration(durationMin)} />
          <Stat label="XP" value={`+${SESSION_XP}`} />
          <Stat label="STREAK" value={`🔥${streak}`} />
        </View>

        {taskLabel ? (
          <KickerLabel style={styles.prompt}>
            {`Did you finish: '${taskLabel}'?`}
          </KickerLabel>
        ) : (
          <KickerLabel style={styles.prompt}>How did it go?</KickerLabel>
        )}

        <TextInput
          value={note}
          onChangeText={setNote}
          placeholder={taskLabel ? `Add a note about '${taskLabel}'…` : 'Add a note…'}
          placeholderTextColor={colors.muted}
          style={styles.input}
          returnKeyType="done"
          maxLength={140}
          multiline
        />

        <View style={styles.chips}>
          {chips.map((c) => {
            const selected = note.trim() === c;
            return (
              <Pressable
                key={c}
                accessibilityRole="button"
                accessibilityState={{ selected }}
                onPress={() => setNote(c)}
                style={[styles.chip, selected && styles.chipSelected]}
              >
                <Text style={[styles.chipText, selected && styles.chipTextSelected]}>
                  {c}
                </Text>
              </Pressable>
            );
          })}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <Button
          label="Save & share my day"
          onPress={save}
          accessibilityHint="Save this session and open the share card"
        />
      </View>
    </Screen>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.stat}>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  flex: {
    flex: 1,
  },
  content: {
    flexGrow: 1,
    paddingTop: spacing.lg,
    paddingBottom: spacing.lg,
  },
  headline: {
    marginTop: spacing.base,
  },
  stats: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing['2xl'],
  },
  stat: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: spacing.lg,
    borderRadius: radius.lg,
    backgroundColor: colors.ink,
  },
  statValue: {
    fontFamily: fontFamily.monoBold,
    fontSize: 22,
    color: colors.amberLight,
  },
  statLabel: {
    fontFamily: fontFamily.mono,
    fontSize: 11,
    letterSpacing: 1.5,
    color: colors.muted,
    marginTop: spacing.xs,
  },
  prompt: {
    marginTop: spacing['2xl'],
  },
  input: {
    minHeight: 64,
    marginTop: spacing.md,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.base,
    paddingBottom: spacing.base,
    fontFamily: fontFamily.display,
    fontSize: 17,
    color: colors.cream,
  },
  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginTop: spacing.base,
  },
  chip: {
    borderRadius: radius.pill,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
    paddingHorizontal: spacing.base,
    paddingVertical: spacing.sm,
  },
  chipSelected: {
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.12)',
  },
  chipText: {
    fontFamily: fontFamily.display,
    fontSize: 14,
    color: colors.muted,
  },
  chipTextSelected: {
    color: colors.amberLight,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
});
