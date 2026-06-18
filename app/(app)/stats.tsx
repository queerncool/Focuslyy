import { ScrollView, StyleSheet, Text, View } from 'react-native';
import Svg, { Rect } from 'react-native-svg';
import { Body, Display, KickerLabel, Screen } from '@/components';
import { formatDuration } from '@/lib/time';
import {
  currentStreak,
  last7Days,
  longestStreak,
  rollingPeriod,
  startOfDay,
  totalMinutes,
  type DayBar,
  type PeriodStat,
} from '@/lib/stats';
import { useSessionsHistoryStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

export default function StatsTab() {
  const sessions = useSessionsHistoryStore((s) => s.sessions);

  const today = rollingPeriod(sessions, 1);
  const week = rollingPeriod(sessions, 7);
  const month = rollingPeriod(sessions, 30);
  const bars = last7Days(sessions);
  const streak = currentStreak(sessions);
  const best = longestStreak(sessions);
  const banked = totalMinutes(sessions);

  const hasData = sessions.length > 0;

  return (
    <Screen style={styles.screen}>
      <ScrollView
        style={styles.flex}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <KickerLabel>Stats</KickerLabel>
        <Display style={styles.headline}>Your deep work, counted.</Display>

        {!hasData ? (
          <View style={styles.firstCard}>
            <Text style={styles.firstEmoji}>🟠</Text>
            <Body color={colors.cream} style={styles.firstTitle}>
              Your first session is the hardest.
            </Body>
            <Body style={styles.firstText}>
              Run one focus block and your hours, streak, and chart start filling
              in right here.
            </Body>
          </View>
        ) : (
          <>
            <View style={styles.periodRow}>
              <PeriodTile label="TODAY" stat={today} />
              <PeriodTile label="THIS WEEK" stat={week} />
              <PeriodTile label="THIS MONTH" stat={month} />
            </View>

            <View style={styles.chartCard}>
              <KickerLabel>Last 7 days</KickerLabel>
              <BarChart bars={bars} />
            </View>

            <View style={styles.streakRow}>
              <StreakTile label="CURRENT STREAK" value={`🔥 ${streak}`} />
              <StreakTile label="BEST STREAK" value={`${best}`} />
              <StreakTile label="BANKED" value={formatDuration(banked)} />
            </View>

            <KickerLabel style={styles.recentHeading}>Recent sessions</KickerLabel>
            <View style={styles.recent}>
              {sessions.slice(0, 8).map((s) => (
                <View key={s.id} style={styles.recentRow}>
                  <View style={styles.recentLeft}>
                    <Text style={styles.recentTask} numberOfLines={1}>
                      {s.task || (s.mode ? `${s.mode} session` : 'Focus session')}
                    </Text>
                    <Text style={styles.recentMeta}>
                      {formatRecentDate(s.startedAt)}
                      {s.completed ? '' : ' · seal broken'}
                    </Text>
                  </View>
                  <Text style={styles.recentDuration}>{formatDuration(s.durationMin)}</Text>
                </View>
              ))}
            </View>
          </>
        )}
      </ScrollView>
    </Screen>
  );
}

function PeriodTile({ label, stat }: { label: string; stat: PeriodStat }) {
  return (
    <View style={styles.periodTile}>
      <Text style={styles.periodLabel}>{label}</Text>
      <Text style={styles.periodValue}>{formatDuration(stat.minutes)}</Text>
      {stat.deltaPct != null && (
        <Text
          style={[
            styles.delta,
            { color: stat.deltaPct >= 0 ? colors.teal : colors.crimson },
          ]}
        >
          {stat.deltaPct >= 0 ? '+' : ''}
          {stat.deltaPct}%
        </Text>
      )}
    </View>
  );
}

function StreakTile({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.streakTile}>
      <Text style={styles.streakValue}>{value}</Text>
      <Text style={styles.streakLabel}>{label}</Text>
    </View>
  );
}

const CHART_HEIGHT = 120;
const BAR_GAP = 10;

function BarChart({ bars }: { bars: DayBar[] }) {
  const max = Math.max(...bars.map((b) => b.minutes), 1);
  const n = bars.length;

  return (
    <View>
      <Svg width="100%" height={CHART_HEIGHT} viewBox={`0 0 100 ${CHART_HEIGHT}`}>
        {bars.map((b, i) => {
          const slot = (100 - BAR_GAP * (n - 1)) / n;
          const x = i * (slot + BAR_GAP);
          const h = Math.max(2, (b.minutes / max) * (CHART_HEIGHT - 8));
          const y = CHART_HEIGHT - h;
          return (
            <Rect
              key={i}
              x={x}
              y={y}
              width={slot}
              height={h}
              rx={3}
              fill={b.isToday ? colors.amber : colors.muted}
              opacity={b.minutes === 0 ? 0.3 : 1}
            />
          );
        })}
      </Svg>
      <View style={styles.barLabels}>
        {bars.map((b, i) => (
          <Text
            key={i}
            style={[styles.barLabel, b.isToday && styles.barLabelToday]}
          >
            {b.label[0]}
          </Text>
        ))}
      </View>
    </View>
  );
}

function formatRecentDate(ts: number): string {
  const today = startOfDay(Date.now());
  const day = startOfDay(ts);
  const diffDays = Math.round((today - day) / 86400000);
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  return new Date(ts).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  flex: {
    flex: 1,
  },
  content: {
    paddingTop: spacing.lg,
    paddingBottom: spacing['2xl'],
  },
  headline: {
    marginTop: spacing.sm,
    marginBottom: spacing.xl,
  },
  firstCard: {
    padding: spacing.xl,
    borderRadius: radius.xl,
    backgroundColor: colors.ink,
    alignItems: 'center',
    gap: spacing.md,
  },
  firstEmoji: {
    fontSize: 36,
  },
  firstTitle: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 20,
    textAlign: 'center',
  },
  firstText: {
    fontSize: 15,
    lineHeight: 22,
    textAlign: 'center',
  },
  periodRow: {
    flexDirection: 'row',
    gap: spacing.sm,
  },
  periodTile: {
    flex: 1,
    padding: spacing.base,
    borderRadius: radius.lg,
    backgroundColor: colors.ink,
    gap: spacing.xs,
  },
  periodLabel: {
    fontFamily: fontFamily.mono,
    fontSize: 10,
    letterSpacing: 1,
    color: colors.muted,
  },
  periodValue: {
    fontFamily: fontFamily.monoBold,
    fontSize: 20,
    color: colors.cream,
  },
  delta: {
    fontFamily: fontFamily.mono,
    fontSize: 12,
  },
  chartCard: {
    marginTop: spacing.base,
    padding: spacing.lg,
    borderRadius: radius.xl,
    backgroundColor: colors.ink,
    gap: spacing.base,
  },
  barLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  barLabel: {
    flex: 1,
    textAlign: 'center',
    fontFamily: fontFamily.mono,
    fontSize: 11,
    color: colors.muted,
  },
  barLabelToday: {
    color: colors.amber,
  },
  streakRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.base,
  },
  streakTile: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: spacing.lg,
    borderRadius: radius.lg,
    backgroundColor: colors.ink,
    gap: spacing.xs,
  },
  streakValue: {
    fontFamily: fontFamily.monoBold,
    fontSize: 18,
    color: colors.amberLight,
  },
  streakLabel: {
    fontFamily: fontFamily.mono,
    fontSize: 9,
    letterSpacing: 1,
    color: colors.muted,
    textAlign: 'center',
  },
  recentHeading: {
    marginTop: spacing['2xl'],
    marginBottom: spacing.md,
  },
  recent: {
    gap: spacing.sm,
  },
  recentRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: spacing.base,
    borderRadius: radius.lg,
    backgroundColor: colors.ink,
    gap: spacing.base,
  },
  recentLeft: {
    flex: 1,
    gap: 2,
  },
  recentTask: {
    fontFamily: fontFamily.display,
    fontSize: 16,
    color: colors.cream,
  },
  recentMeta: {
    fontFamily: fontFamily.mono,
    fontSize: 12,
    color: colors.muted,
  },
  recentDuration: {
    fontFamily: fontFamily.monoBold,
    fontSize: 15,
    color: colors.amberLight,
  },
});
