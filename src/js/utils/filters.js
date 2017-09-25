function truncate(value, length, omission) {
  const lengthInt = length ? parseInt(length, 10) : 20;
  const ommisionString = omission ? omission.toString() : '...';

  if (value.length <= lengthInt) {
    return value;
  } else {
    return value.substring(0, lengthInt) + ommisionString;
  }
}

export default function registerFilters(vue) {
  vue.filter('truncate', truncate);
}
