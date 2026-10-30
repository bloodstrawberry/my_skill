import { notFound } from 'next/navigation';
import { ToolWorkspace } from '@/components/tool-workspace';
const slugs = ['documents', 'spreadsheets', 'pdf', 'text', 'images', 'media'];
export function generateStaticParams() { return slugs.map(slug => ({ slug })); }
export default async function ToolPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (!slugs.includes(slug)) notFound();
  return <ToolWorkspace slug={slug} />;
}
