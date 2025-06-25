<script lang="ts">
type LinkInfo = {
  title: string,
  url?: string,
  tip?: string,
  needCode?: boolean

}
import { ref, type Component } from 'vue';
type GroupInfo = {
  title: string,
  icon: Component
  links: LinkInfo[]
}
</script>
<script setup lang="ts">
import { ElMenu, ElSubMenu, ElMenuItem, ElIcon, ElButton } from 'element-plus';
import * as Icons from '@element-plus/icons-vue';
import { options } from '../Links.vue';

import menuGroup from './menu_group.json'; 

function onSelected(key: string) {
    const [groupIndex, linkIndex] = key.split('-').map(Number)
    const link: LinkInfo = menuGroup[groupIndex]?.links[linkIndex]
    if (link && link?.url) {
        if (link.needCode && options.code) {
            link.url = link.url.replace('{code}', options.code)
        }
        options.target = link.url
    }
    console.log('target', options.target)
}

function checkDisabled(link: LinkInfo): boolean {
    if (link.url === undefined) {
        return true
    }
    if (link.needCode && !options.code) {
        return true
    }
    return false
}
</script>
<template>
    <ElMenu
        default-active="0-0"
        :collapse="options.collapse"
        class="el-menu-vertical"
        @select="onSelected">
        <ElSubMenu v-for="(group, gindex) in menuGroup" :key="gindex" :index="gindex.toString()">
            <template #title>
                <ElIcon>
                    <component :is="Icons[group.icon]" />
                </ElIcon>
                <span style="font-weight: bold;">{{ group.title }}</span>
            </template>
            <ElMenuItem v-for="(link, index) in group.links" :key="index" :index="gindex.toString() + '-' + index.toString()">
                <!-- <a :href="link.url" target="_blank" rel="noopener noreferrer">{{ link.title }} </a> -->
                <template #title>
                    <ElButton :link="true" :disabled="checkDisabled(link)" > {{ link.title }}</ElButton>
                </template>                
            </ElMenuItem>
        </ElSubMenu>
    </ElMenu>
</template>
<style>
.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
