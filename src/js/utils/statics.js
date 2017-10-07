import path from 'path';

function getStaticPath() {
  if (process.env.NODE_ENV === 'production') {
    return 'https://s3-ap-northeast-1.amazonaws.com/jaaxman-production-assets/';
  } else {
    return '/static';
  }
}

export function getImgPath(filename) {
  const staticPath = getStaticPath();
  return path.join(staticPath, 'img', filename);
}
