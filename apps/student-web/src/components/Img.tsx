/* eslint-disable @next/next/no-img-element */
// Single place for plain <img> usage: assets are pre-optimised WebP/PNG served from /public.
export default function Img(props: React.ImgHTMLAttributes<HTMLImageElement> & { alt: string }) {
  return <img loading="lazy" decoding="async" {...props} />;
}
