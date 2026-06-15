/** Asset module declarations so TypeScript accepts require()'d font/image files. */
declare module '*.ttf' {
  const asset: number;
  export default asset;
}

declare module '*.otf' {
  const asset: number;
  export default asset;
}
