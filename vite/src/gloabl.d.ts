export {};

declare global {
  interface Window {
    bookmarklet: {
      siteUrl: string;
      launch: () => void;
    };
  }
}
