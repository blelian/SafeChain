// frontend/pages/_app.tsx
import '../styles/globals.css';
import type { AppProps } from 'next/app';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-gray-900 via-emerald-900 to-gray-800">
      <Component {...pageProps} />
    </div>
  );
}
