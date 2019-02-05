export function isHidden(element) {
  if (element.offsetParent === null) return true;
  const style = getComputedStyle(element);
  return style.display.toLowerCase() === 'none'
    || style.visibility.toLowerCase() === 'hidden';
}

export function zebrafy(element) {
  // QnD hack for zebra stripes
  const zebraElements = ([].slice.call(element.getElementsByClassName('zebra')))
    .filter(element => !isHidden(element));
  var counter = 0;
  zebraElements.forEach(element => {
    element.classList.remove('even');
    element.classList.remove('odd');
    if (counter % 2 == 0) {
      element.classList.add('even');
    } else {
      element.classList.add('odd');
    }
    counter++;
  });
}
