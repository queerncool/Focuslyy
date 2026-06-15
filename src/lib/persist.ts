import AsyncStorage from '@react-native-async-storage/async-storage';
import { createJSONStorage } from 'zustand/middleware';

/**
 * Shared AsyncStorage adapter for all persisted Zustand stores.
 * Keeps the storage engine in one place so v1 persistence is uniform.
 */
export const asyncStorage = createJSONStorage(() => AsyncStorage);

/** Namespaced key helper so all focuslyy keys share a prefix. */
export const storeKey = (name: string) => `focuslyy.${name}`;
