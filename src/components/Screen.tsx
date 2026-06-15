import type { ReactNode } from 'react';
import {
  StyleSheet,
  View,
  type StyleProp,
  type ViewStyle,
} from 'react-native';
import { SafeAreaView, type Edge } from 'react-native-safe-area-context';
import { colors } from '@/theme';

interface ScreenProps {
  children: ReactNode;
  /** Background tone. Most app surfaces are dark (espresso). */
  tone?: 'dark' | 'light';
  /** Center children both axes (handy for placeholders/empty states). */
  center?: boolean;
  edges?: readonly Edge[];
  style?: StyleProp<ViewStyle>;
}

/** Safe-area screen container with a locked background color. */
export function Screen({
  children,
  tone = 'dark',
  center = false,
  edges = ['top', 'bottom'],
  style,
}: ScreenProps) {
  return (
    <SafeAreaView
      edges={edges}
      style={[
        styles.base,
        { backgroundColor: tone === 'dark' ? colors.espresso : colors.cream },
      ]}
    >
      <View style={[styles.inner, center && styles.center, style]}>
        {children}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  base: {
    flex: 1,
  },
  inner: {
    flex: 1,
  },
  center: {
    alignItems: 'center',
    justifyContent: 'center',
  },
});
