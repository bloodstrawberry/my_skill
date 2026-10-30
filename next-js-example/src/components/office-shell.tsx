'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { alpha, createTheme, ThemeProvider } from '@mui/material/styles';
import { Box, Button, Chip, CssBaseline, Dialog, DialogContent, DialogTitle, Divider, Drawer, IconButton, InputAdornment, List, ListItemButton, ListItemIcon, ListItemText, Stack, TextField, Tooltip, Typography } from '@mui/material';
import MenuRounded from '@mui/icons-material/MenuRounded';
import SearchRounded from '@mui/icons-material/SearchRounded';
import DashboardRounded from '@mui/icons-material/DashboardRounded';
import DarkModeRounded from '@mui/icons-material/DarkModeRounded';
import LightModeRounded from '@mui/icons-material/LightModeRounded';
import ChevronLeftRounded from '@mui/icons-material/ChevronLeftRounded';
import ChevronRightRounded from '@mui/icons-material/ChevronRightRounded';
import CloseRounded from '@mui/icons-material/CloseRounded';
import { tools } from '@/lib/tools';

const SearchContext = createContext(() => {});
export const useToolSearch = () => useContext(SearchContext);

export function OfficeShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [dark, setDark] = useState(false);
  const [mini, setMini] = useState(false);
  const [mobile, setMobile] = useState(false);
  const [search, setSearch] = useState(false);
  const [query, setQuery] = useState('');
  useEffect(() => {
    try { setDark(localStorage.getItem('office:dark') === 'true'); setMini(localStorage.getItem('office:mini') === 'true'); } catch { /* Storage may be disabled. */ }
    const keydown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); setSearch(value => !value); }
    };
    window.addEventListener('keydown', keydown);
    return () => window.removeEventListener('keydown', keydown);
  }, []);
  const toggle = (key: string, value: boolean, update: (value: boolean) => void) => {
    update(value); try { localStorage.setItem(key, String(value)); } catch { /* State still works in memory. */ }
  };
  const theme = useMemo(() => createTheme({
    palette: { mode: dark ? 'dark' : 'light', primary: { main: dark ? '#5be49b' : '#007b55' }, background: { default: dark ? '#141a21' : '#f6f8fa', paper: dark ? '#1c252e' : '#ffffff' }, text: { primary: dark ? '#f3f5f7' : '#1c252e', secondary: dark ? '#a5b0bd' : '#637381' } },
    shape: { borderRadius: 12 },
    typography: { fontFamily: 'Arial, "Malgun Gothic", sans-serif', h4: { fontWeight: 800 }, h6: { fontWeight: 700 }, button: { textTransform: 'none', fontWeight: 700 } },
    components: { MuiButton: { defaultProps: { disableElevation: true } }, MuiCard: { styleOverrides: { root: { borderRadius: 20, boxShadow: 'none' } } }, MuiListItemButton: { styleOverrides: { root: { borderRadius: 10 } } } },
  }), [dark]);
  const current = tools.find(tool => pathname === `/tools/${tool.slug}`);
  const navigation = (compact: boolean) => <Stack sx={{ height: '100%', p: 2 }}>
    <Stack direction="row" alignItems="center" spacing={1.2} sx={{ height: 54, mb: 3 }}>
      <Box component={Link} href="/" aria-label="Ultra Office 홈" sx={{ display: 'grid', placeItems: 'center', width: 38, height: 38, borderRadius: 2, bgcolor: 'primary.main', color: 'primary.contrastText', fontWeight: 900, flexShrink: 0 }}>U</Box>
      {!compact && <Box><Typography fontWeight={800}>Ultra Office</Typography><Typography variant="caption" color="text.secondary">YOUR WORKSPACE</Typography></Box>}
    </Stack>
    {!compact && <Typography variant="overline" color="text.secondary" sx={{ px: 1.5, mb: 1 }}>작업 공간</Typography>}
    <List disablePadding sx={{ display: 'grid', gap: .6 }}>
      {[{ slug: '', title: '전체 도구', icon: DashboardRounded }, ...tools].map(item => {
        const href = item.slug ? `/tools/${item.slug}` : '/';
        return <Tooltip key={href} title={compact ? item.title : ''} placement="right"><ListItemButton component={Link} href={href} selected={pathname === href} aria-label={item.title} aria-current={pathname === href ? 'page' : undefined} onClick={() => setMobile(false)} sx={{ minHeight: 48, px: 1.5, '&.Mui-selected': { color: 'primary.main', bgcolor: alpha(theme.palette.primary.main, .1) } }}>
          <ListItemIcon sx={{ minWidth: compact ? 0 : 36, color: 'inherit' }}><item.icon fontSize="small" /></ListItemIcon>
          {!compact && <ListItemText primary={item.title} slotProps={{ primary: { fontSize: 14, fontWeight: 600 } }} />}
        </ListItemButton></Tooltip>;
      })}
    </List>
    <Box sx={{ flex: 1 }} />
    {!compact && <Box sx={{ bgcolor: 'background.default', borderRadius: 3, p: 2, mt: 3 }}><Typography variant="subtitle2">나만의 업무 공간</Typography><Typography variant="caption" color="text.secondary">필요한 도구를 선택해 시작하세요.</Typography></Box>}
    <Divider sx={{ my: 2 }} />
    <Typography variant="caption" color="text.secondary" textAlign="center">{compact ? 'UO' : 'Ultra Office · UI Starter'}</Typography>
  </Stack>;
  return <ThemeProvider theme={theme}><CssBaseline /><SearchContext.Provider value={() => setSearch(true)}>
    <Box sx={{ display: 'flex', height: '100dvh', overflow: 'hidden' }}>
      <Box component="aside" aria-label="주 메뉴" sx={{ width: mini ? 80 : 272, flexShrink: 0, display: { xs: 'none', md: 'block' }, bgcolor: 'background.paper', borderRight: 1, borderColor: 'divider', position: 'relative' }}>
        {navigation(mini)}
        <Tooltip title={mini ? '메뉴 펼치기' : '메뉴 접기'}><IconButton aria-label={mini ? '메뉴 펼치기' : '메뉴 접기'} size="small" onClick={() => toggle('office:mini', !mini, setMini)} sx={{ position: 'absolute', right: -14, top: 84, zIndex: 2, bgcolor: 'background.paper', border: 1, borderColor: 'divider' }}>{mini ? <ChevronRightRounded fontSize="small" /> : <ChevronLeftRounded fontSize="small" />}</IconButton></Tooltip>
      </Box>
      <Drawer open={mobile} onClose={() => setMobile(false)} slotProps={{ paper: { sx: { width: 280 } } }}><Box sx={{ textAlign: 'right', px: 1, pt: 1 }}><IconButton aria-label="메뉴 닫기" onClick={() => setMobile(false)}><CloseRounded /></IconButton></Box>{navigation(false)}</Drawer>
      <Box sx={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <Stack component="header" direction="row" alignItems="center" spacing={2} sx={{ minHeight: 76, px: { xs: 2, md: 5 }, bgcolor: 'background.paper', borderBottom: 1, borderColor: 'divider' }}>
          <IconButton aria-label="메뉴 열기" onClick={() => setMobile(true)} sx={{ display: { md: 'none' } }}><MenuRounded /></IconButton>
          <Typography variant="body2" color="text.secondary" sx={{ flex: 1 }}>워크스페이스 <Box component="span" sx={{ mx: 1 }}> / </Box><Box component="span" sx={{ color: 'text.primary', fontWeight: 600 }}>{current?.title ?? '전체 도구'}</Box></Typography>
          <Button color="inherit" startIcon={<SearchRounded />} onClick={() => setSearch(true)} aria-label="도구 검색" sx={{ minWidth: 40 }}><Box component="span" sx={{ display: { xs: 'none', sm: 'inline' } }}>검색 <Chip label="Ctrl K" size="small" sx={{ ml: 1 }} /></Box></Button>
          <Tooltip title={dark ? '라이트 모드' : '다크 모드'}><IconButton aria-label={dark ? '라이트 모드' : '다크 모드'} onClick={() => toggle('office:dark', !dark, setDark)}>{dark ? <LightModeRounded /> : <DarkModeRounded />}</IconButton></Tooltip>
        </Stack>
        <Box component="main" id="main-content" sx={{ flex: 1, minHeight: 0, overflow: 'auto', p: { xs: 2, sm: 3, md: 5 }, pb: 'max(24px, env(safe-area-inset-bottom))' }}>{children}</Box>
      </Box>
    </Box>
    <Dialog open={search} onClose={() => setSearch(false)} fullWidth maxWidth="sm" aria-labelledby="search-title">
      <DialogTitle id="search-title" sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>도구 검색<IconButton aria-label="검색 닫기" onClick={() => setSearch(false)}><CloseRounded /></IconButton></DialogTitle>
      <DialogContent><TextField autoFocus fullWidth placeholder="이름 또는 카테고리 검색" value={query} onChange={event => setQuery(event.target.value)} slotProps={{ htmlInput: { 'aria-label': '도구 검색어' }, input: { startAdornment: <InputAdornment position="start"><SearchRounded /></InputAdornment> } }} />
        <List>{tools.filter(tool => `${tool.title} ${tool.category}`.includes(query.trim())).map(tool => <ListItemButton key={tool.slug} onClick={() => { router.push(`/tools/${tool.slug}`); setSearch(false); setQuery(''); }}><ListItemIcon><tool.icon /></ListItemIcon><ListItemText primary={tool.title} secondary={tool.description} /></ListItemButton>)}</List>
        {!tools.some(tool => `${tool.title} ${tool.category}`.includes(query.trim())) && <Typography color="text.secondary" sx={{ py: 3 }}>검색 결과가 없습니다. 다른 검색어를 입력해 주세요.</Typography>}
      </DialogContent>
    </Dialog>
  </SearchContext.Provider></ThemeProvider>;
}
