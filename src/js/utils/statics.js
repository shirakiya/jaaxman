import path from 'path';

function getStaticPath() {
  if (process.env.NODE_ENV === 'production') {
    return '';  // TODO
  } else {
    return '/static';
  }
}

export function getImgPath(filename) {
  const staticPath = getStaticPath();
  return path.join(staticPath, 'img', filename);
}
