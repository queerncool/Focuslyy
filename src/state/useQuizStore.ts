import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { asyncStorage, storeKey } from '@/lib/persist';
import type { Distraction, HoursBand, Mode } from '@/types';

/** §D quizStore — onboarding answers + derived values (§C bindings). */
interface QuizState {
  hoursBand: HoursBand | null;
  hoursNum: number | null; // band midpoint (1, 3, 5, 7)
  yrNum: number | null; // hoursNum × 365, rounded to nearest hundred
  barH: number | null; // bar height ratio vs cited 4.62 avg
  distractions: Distraction[];
  mode: Mode | null;
  projection: string | null;

  setHours: (band: HoursBand, hoursNum: number, yrNum: number, barH: number) => void;
  toggleDistraction: (d: Distraction) => void;
  setGoal: (mode: Mode, projection: string) => void;
  reset: () => void;
}

const initial = {
  hoursBand: null,
  hoursNum: null,
  yrNum: null,
  barH: null,
  distractions: [] as Distraction[],
  mode: null,
  projection: null,
};

export const useQuizStore = create<QuizState>()(
  persist(
    (set) => ({
      ...initial,
      setHours: (hoursBand, hoursNum, yrNum, barH) =>
        set({ hoursBand, hoursNum, yrNum, barH }),
      toggleDistraction: (d) =>
        set((s) => ({
          distractions: s.distractions.includes(d)
            ? s.distractions.filter((x) => x !== d)
            : [...s.distractions, d],
        })),
      setGoal: (mode, projection) => set({ mode, projection }),
      reset: () => set(initial),
    }),
    { name: storeKey('quiz'), storage: asyncStorage }
  )
);
