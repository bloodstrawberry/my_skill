'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Box, Button, Card, CardActionArea, Chip, Stack, Typography } from '@mui/material';
import ArrowForwardRounded from '@mui/icons-material/ArrowForwardRounded';
import SearchRounded from '@mui/icons-material/SearchRounded';
import { tools } from '@/lib/tools';
import { useToolSearch } from '@/components/office-shell';

export default function HomePage() {
  const [category, setCategory] = useState('전체');
  const openSearch = useToolSearch();
  return <Box sx={{ maxWidth: 1400, mx: 'auto' }}>
    <Box sx={{ mb: 4 }}><Typography variant="overline" color="primary.main" fontWeight={800}>WORK BETTER, TOGETHER</Typography><Typography variant="h4" sx={{ mt: 1, fontSize: { xs: 27, md: 34 } }}>오늘의 업무, 한곳에서.</Typography><Typography color="text.secondary" sx={{ mt: 1.5 }}>문서부터 데이터까지, 필요한 작업 공간을 선택하세요.</Typography></Box>
    <Box sx={{ p: { xs: 3, md: 4 }, borderRadius: 5, mb: 5, bgcolor: 'primary.main', color: 'primary.contrastText', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 3, flexWrap: 'wrap' }}>
      <Box><Chip label="ULTRA OFFICE" size="small" sx={{ mb: 2, bgcolor: 'rgba(255,255,255,.17)', color: 'inherit', fontWeight: 700 }} /><Typography variant="h5" fontWeight={700}>필요한 도구를 빠르게 찾아보세요</Typography><Typography sx={{ mt: 1, opacity: .85 }}>가벼운 시작, 익숙한 작업 공간.</Typography></Box>
      <Button variant="contained" startIcon={<SearchRounded />} onClick={openSearch} sx={{ bgcolor: 'background.paper', color: 'text.primary', px: 3, py: 1.5, '&:hover': { bgcolor: 'background.default' } }}>도구 검색</Button>
    </Box>
    <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}><Typography variant="h6">모든 작업 공간</Typography><Typography variant="body2" color="text.secondary">{tools.filter(tool => category === '전체' || tool.category === category).length}개 도구</Typography></Stack>
    <Stack direction="row" gap={1} useFlexGap flexWrap="wrap" sx={{ mb: 3 }}>{['전체', '문서', '데이터', '텍스트', '미디어'].map(item => <Chip key={item} label={item} onClick={() => setCategory(item)} color={category === item ? 'primary' : 'default'} variant={category === item ? 'filled' : 'outlined'} aria-pressed={category === item} />)}</Stack>
    <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', xl: 'repeat(3, 1fr)' }, gap: 2.5 }}>
      {tools.filter(tool => category === '전체' || tool.category === category).map(tool => <Card key={tool.slug} variant="outlined"><CardActionArea component={Link} href={`/tools/${tool.slug}`} sx={{ p: 3, height: '100%', '&:hover .tool-arrow': { transform: 'translateX(4px)' } }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 3 }}><Box sx={{ display: 'grid', placeItems: 'center', width: 52, height: 52, borderRadius: 3, bgcolor: `${tool.color}18`, color: tool.color }}><tool.icon /></Box><Chip label={tool.category} size="small" variant="outlined" /></Stack>
        <Typography variant="h6" sx={{ mb: 1 }}>{tool.title}</Typography><Typography variant="body2" color="text.secondary">{tool.description}</Typography>
        <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 3 }}><Typography variant="body2" fontWeight={700}>작업 공간 열기</Typography><ArrowForwardRounded className="tool-arrow" sx={{ fontSize: 18, transition: 'transform .2s' }} /></Stack>
      </CardActionArea></Card>)}
    </Box>
    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 4 }}>UI 미리보기 · 파일 처리 기능은 아직 연결되지 않았습니다.</Typography>
  </Box>;
}
