function truncate(value, length = 20, omission = '...') {
  const lengthInt = parseInt(length, 10);

  if (value.length <= lengthInt) {
    return value;
  } else {
    return value.substring(0, lengthInt) + omission;
  }
}

export default function registerFilters(vue) {
  vue.filter('truncate', truncate);
}
