/* global process  */

function getStaticPath() {
  if (process.env.NODE_ENV === 'production') {
    return 'https://s3-ap-northeast-1.amazonaws.com/jaaxman-production-public';
  } else {
    return '/static';
  }
}

export function getImgPath(filename) {
  const staticPath = getStaticPath();
  return `${staticPath}/img/${filename}`;
}
