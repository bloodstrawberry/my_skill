import DescriptionRounded from '@mui/icons-material/DescriptionRounded';
import TableChartRounded from '@mui/icons-material/TableChartRounded';
import PictureAsPdfRounded from '@mui/icons-material/PictureAsPdfRounded';
import TextFieldsRounded from '@mui/icons-material/TextFieldsRounded';
import ImageRounded from '@mui/icons-material/ImageRounded';
import VideoLibraryRounded from '@mui/icons-material/VideoLibraryRounded';

// UI navigation only. Processing engines are intentionally not imported.
export const tools = [
  { slug: 'documents', title: '문서 작업실', category: '문서', description: '문서와 보고서를 위한 작업 공간', icon: DescriptionRounded, color: '#6370d5' },
  { slug: 'spreadsheets', title: '스프레드시트', category: '데이터', description: '표와 데이터를 한눈에 살펴보는 공간', icon: TableChartRounded, color: '#00a76f' },
  { slug: 'pdf', title: 'PDF 작업실', category: '문서', description: 'PDF 문서를 위한 작업 공간', icon: PictureAsPdfRounded, color: '#e45d56' },
  { slug: 'text', title: '텍스트 도구', category: '텍스트', description: '텍스트를 정리하고 비교하는 공간', icon: TextFieldsRounded, color: '#b27b20' },
  { slug: 'images', title: '이미지 작업실', category: '미디어', description: '이미지 자료를 위한 작업 공간', icon: ImageRounded, color: '#008fa8' },
  { slug: 'media', title: '오디오 · 비디오', category: '미디어', description: '음성과 영상을 위한 작업 공간', icon: VideoLibraryRounded, color: '#a05fc2' },
];
