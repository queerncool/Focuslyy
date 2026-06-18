import { useEffect, useState } from 'react';
import { router } from 'expo-router';
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  Pill,
  Screen,
  SegmentedOption,
} from '@/components';
import {
  BLOCK_LENGTHS,
  MAX_CUSTOM_MIN,
  tasksForMode,
} from '@/lib/session';
import { useQuizStore, useSessionStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

const LENGTH_OPTIONS = BLOCK_LENGTHS.map((m) => ({ value: m, label: String(m) }));

export default function SetSession() {
  const mode = useQuizStore((s) => s.mode);

  const task = useSessionStore((s) => s.task);
  const blockMin = useSessionStore((s) => s.blockMin);
  const setTask = useSessionStore((s) => s.setTask);
  const setBlockMin = useSessionStore((s) => s.setBlockMin);
  const setMode = useSessionStore((s) => s.setMode);

  // Custom length is shown when the active blockMin isn't one of the presets.
  const presetActive = (BLOCK_LENGTHS as readonly number[]).includes(blockMin);
  const [customText, setCustomText] = useState(presetActive ? '' : String(blockMin));

  // Carry the onboarding mode into the session record.
  useEffect(() => {
    setMode(mode);
  }, [mode, setMode]);

  const onCustomChange = (text: string) => {
    const digits = text.replace(/[^0-9]/g, '').slice(0, 3);
    setCustomText(digits);
    const n = parseInt(digits, 10);
    if (!Number.isNaN(n) && n > 0) {
      setBlockMin(Math.min(n, MAX_CUSTOM_MIN));
    }
  };

  const onPreset = (value: number) => {
    setCustomText('');
    setBlockMin(value);
  };

  const tasks = tasksForMode(mode);

  return (
    <Screen style={styles.screen}>
      <ScrollView
        style={styles.flex}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.headerRow}>
          <KickerLabel>Set session</KickerLabel>
          {mode != null && <Pill label={`${mode} mode`} tone="amber" />}
        </View>

        <Display style={styles.headline}>
          What's the one thing that matters most right now?
        </Display>

        <TextInput
          value={task}
          onChangeText={setTask}
          placeholder="Name your one thing"
          placeholderTextColor={colors.muted}
          style={styles.input}
          returnKeyType="done"
          maxLength={80}
          multiline
        />

        <View style={styles.chips}>
          {tasks.map((t) => {
            const selected = task.trim() === t;
            return (
              <Pressable
                key={t}
                accessibilityRole="button"
                accessibilityState={{ selected }}
                accessibilityHint="Use this as your task"
                onPress={() => setTask(t)}
                style={[styles.chip, selected && styles.chipSelected]}
              >
                <Text style={[styles.chipText, selected && styles.chipTextSelected]}>
                  {t}
                </Text>
              </Pressable>
            );
          })}
        </View>

        <View style={styles.field}>
          <KickerLabel>Block length (min)</KickerLabel>
          <SegmentedOption
            options={LENGTH_OPTIONS}
            value={presetActive ? blockMin : -1}
            onChange={onPreset}
          />
          <TextInput
            value={customText}
            onChangeText={onCustomChange}
            placeholder={`Custom — up to ${MAX_CUSTOM_MIN} min`}
            placeholderTextColor={colors.muted}
            style={styles.customInput}
            keyboardType="number-pad"
            returnKeyType="done"
            maxLength={3}
          />
          <Body style={styles.lengthNote}>
            Sealing for {blockMin} min.
          </Body>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <Button
          label="Choose what to block →"
          onPress={() => router.push('/sealApps')}
          accessibilityHint="Pick the apps to seal for this session"
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
  content: {
    flexGrow: 1,
    paddingTop: spacing.lg,
    paddingBottom: spacing.lg,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  headline: {
    marginTop: spacing.base,
  },
  input: {
    minHeight: 64,
    marginTop: spacing.xl,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.base,
    paddingBottom: spacing.base,
    fontFamily: fontFamily.display,
    fontSize: 18,
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
  field: {
    marginTop: spacing['2xl'],
    gap: spacing.md,
  },
  customInput: {
    minHeight: 52,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
    paddingHorizontal: spacing.lg,
    fontFamily: fontFamily.mono,
    fontSize: 16,
    color: colors.cream,
  },
  lengthNote: {
    fontFamily: fontFamily.mono,
    fontSize: 13,
    color: colors.muted,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
});
