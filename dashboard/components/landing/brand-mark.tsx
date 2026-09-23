export function BrandMark({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M12 3.2C8.2 5.1 5.8 8.8 5.8 12.8c0 3.4 2.2 6.3 6.2 8 4-1.7 6.2-4.6 6.2-8 0-4-2.4-7.7-6.2-9.6Z"
        stroke="currentColor"
        strokeWidth="1.4"
      />
      <circle cx="12" cy="12.4" r="2.1" fill="currentColor" />
      <path d="M7.2 11.2h9.6" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
    </svg>
  );
}
