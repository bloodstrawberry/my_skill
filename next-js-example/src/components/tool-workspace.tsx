'use client';
import Link from 'next/link';
import { Box, Button, Chip, Paper, Stack, Typography } from '@mui/material';
import ArrowBackRounded from '@mui/icons-material/ArrowBackRounded';
import { tools } from '@/lib/tools';
export function ToolWorkspace({ slug }: { slug: string }) {
  const tool = tools.find(item => item.slug === slug)!;
  return <Stack spacing={3} sx={{ minHeight: '100%', maxWidth: 1400, mx: 'auto' }}>
    <Box><Button component={Link} href="/" color="inherit" startIcon={<ArrowBackRounded />} sx={{ mb: 2 }}>전체 도구</Button><Stack direction="row" spacing={2} alignItems="center"><Typography variant="h4">{tool.title}</Typography><Chip label="준비 중" size="small" /></Stack><Typography color="text.secondary" sx={{ mt: 1.5 }}>{tool.description}</Typography></Box>
    <Paper variant="outlined" sx={{ flex: 1, minHeight: 340, borderRadius: 4, display: 'grid', placeItems: 'center', p: 3 }}><Stack alignItems="center" textAlign="center" spacing={2} sx={{ maxWidth: 390 }}><Box sx={{ width: 76, height: 76, display: 'grid', placeItems: 'center', bgcolor: `${tool.color}18`, color: tool.color, borderRadius: 4 }}><tool.icon sx={{ fontSize: 36 }} /></Box><Typography variant="h6">작업 공간이 준비되었습니다</Typography><Typography color="text.secondary" variant="body2">현재는 기본 화면만 제공됩니다. 파일 업로드와 처리 기능은 추후 연결됩니다.</Typography><Button disabled variant="contained">파일 처리 준비 중</Button></Stack></Paper>
  </Stack>;
}
