import type { Metadata } from 'next';
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
import { OfficeShell } from '@/components/office-shell';
import './globals.css';

export const metadata: Metadata = {
  title: { default: 'Ultra Office · Workspace', template: '%s · Ultra Office' },
  description: 'MUI 기반 업무 도구 UI 스타터',
};
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="ko"><body><AppRouterCacheProvider>
    <OfficeShell>{children}</OfficeShell>
  </AppRouterCacheProvider></body></html>;
}
