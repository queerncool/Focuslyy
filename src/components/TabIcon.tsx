import Svg, { Circle, Path, Rect } from 'react-native-svg';
import { colors } from '@/theme';

export type TabName = 'focus' | 'friends' | 'stats' | 'profile';

interface TabIconProps {
  name: TabName;
  focused: boolean;
  size?: number;
}

/**
 * Minimal line-glyph tab icons drawn with react-native-svg so we stay on the
 * locked palette and avoid platform-specific symbol sets.
 */
export function TabIcon({ name, focused, size = 24 }: TabIconProps) {
  const stroke = focused ? colors.amber : colors.muted;
  const sw = 2;

  switch (name) {
    case 'focus':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Circle cx={12} cy={12} r={9} stroke={stroke} strokeWidth={sw} />
          <Circle cx={12} cy={12} r={3} fill={stroke} />
        </Svg>
      );
    case 'friends':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Circle cx={9} cy={8} r={3.2} stroke={stroke} strokeWidth={sw} />
          <Path
            d="M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5"
            stroke={stroke}
            strokeWidth={sw}
            strokeLinecap="round"
          />
          <Path
            d="M16 6.5a3 3 0 0 1 0 6M17 14c2.4.3 4.5 2.2 4.5 5"
            stroke={stroke}
            strokeWidth={sw}
            strokeLinecap="round"
          />
        </Svg>
      );
    case 'stats':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Rect x={4} y={12} width={4} height={7} rx={1} fill={stroke} />
          <Rect x={10} y={8} width={4} height={11} rx={1} fill={stroke} />
          <Rect x={16} y={4} width={4} height={15} rx={1} fill={stroke} />
        </Svg>
      );
    case 'profile':
      return (
        <Svg width={size} height={size} viewBox="0 0 24 24" fill="none">
          <Circle cx={12} cy={8} r={3.6} stroke={stroke} strokeWidth={sw} />
          <Path
            d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6"
            stroke={stroke}
            strokeWidth={sw}
            strokeLinecap="round"
          />
        </Svg>
      );
  }
}
