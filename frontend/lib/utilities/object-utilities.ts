export function deepEqual(obj1: any, obj2: any): boolean {
  // If both objects are null or undefined, they are considered equal
  if (
    obj1 === null ||
    obj1 === undefined ||
    obj2 === null ||
    obj2 === undefined
  ) {
    return obj1 === obj2;
  }

  // If the types of obj1 and obj2 are different, they are not equal
  if (typeof obj1 !== typeof obj2) {
    return false;
  }

  // If obj1 and obj2 are not objects, directly compare their values
  if (typeof obj1 !== "object") {
    return obj1 === obj2;
  }

  // If obj1 and obj2 are arrays, compare their lengths and elements recursively
  if (Array.isArray(obj1)) {
    if (!Array.isArray(obj2) || obj1.length !== obj2.length) {
      return false;
    }
    for (let i = 0; i < obj1.length; i++) {
      if (!deepEqual(obj1[i], obj2[i])) {
        return false;
      }
    }
    return true;
  }

  // If obj1 and obj2 are objects, compare their keys and values recursively
  const keys1 = Object.keys(obj1);
  const keys2 = Object.keys(obj2);
  if (keys1.length !== keys2.length) {
    return false;
  }
  for (const key of keys1) {
    if (!keys2.includes(key) || !deepEqual(obj1[key], obj2[key])) {
      return false;
    }
  }
  return true;
}
