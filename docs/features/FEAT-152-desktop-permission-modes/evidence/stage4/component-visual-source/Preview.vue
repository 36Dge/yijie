<script setup lang="ts">
import { ref } from 'vue';
import { NConfigProvider, darkTheme } from 'naive-ui';
import ChatPermissionControl from '../../../src/components/chat/ChatPermissionControl.vue';
import { createNaiveThemeOverrides } from '../../../src/design/theme/naive-theme';
import type { ChatPermissionState, PermissionMode } from '../../../src/api/runtime-permission-client';
const dark = new URLSearchParams(location.search).get('theme') === 'dark';
document.documentElement.dataset.theme = dark ? 'dark' : 'light';
const styles = getComputedStyle(document.documentElement);
const overrides = createNaiveThemeOverrides(name => styles.getPropertyValue(name));
const state = ref<ChatPermissionState>({ mode:'ask', busy:false, fullAccessConfirmed:false });
function select(mode: PermissionMode, confirmed: boolean) {
  state.value = { ...state.value, mode, fullAccessConfirmed:state.value.fullAccessConfirmed || confirmed };
}
</script>
<template>
  <NConfigProvider :theme="dark ? darkTheme : null" :theme-overrides="overrides">
    <main class="canvas">
      <header><strong>FEAT-152 · 生产权限组件视觉检查</strong><p>1180 × 760 布局；仅组件状态，不连接 Native、Host 或 Runtime。</p><a href="?theme=light">浅色</a> · <a href="?theme=dark">深色</a><p>已选择：{{ state.mode }}；首次确认记录：{{ state.fullAccessConfirmed }}</p></header>
      <section class="composer-frame"><p>权限菜单与确认弹窗使用未复制、未改写的生产组件。</p><div class="toolbar"><span aria-hidden="true">＋</span><ChatPermissionControl :state="state" :disabled="false" :saving="false" @select="select" /></div></section>
    </main>
  </NConfigProvider>
</template>
<style scoped>
.canvas { width:1180px; height:760px; position:relative; background:var(--yj-color-bg-app); color:var(--yj-color-text-primary); }
header { padding:24px; font-size:14px; }
header p { color:var(--yj-color-text-secondary); }
a { color:var(--yj-color-text-primary); }
.composer-frame { position:absolute; left:272px; right:32px; bottom:32px; padding:16px; border:1px solid var(--yj-color-border-control); border-radius:16px; }
.composer-frame p { margin:0 0 36px; color:var(--yj-color-text-secondary); }
.toolbar { display:flex; align-items:center; gap:16px; }
.toolbar>span { font-size:24px; }
</style>
