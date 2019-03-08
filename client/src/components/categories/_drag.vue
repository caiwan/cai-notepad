<template>
  <div class="playground">
    <div class="card-placeholder tpl-placeholder">
    </div>
    <!-- cards to sort -->
    <div
      class="card"
      draggable="true"
    >
      <img
        width="250"
        height="150"
        src="https://source.unsplash.com/random/250x150"
        draggable="false"
      />
      <div class="card-text">
        <h3>Some Title</h3>
        <span>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam...</span>
      </div>
    </div>
    <div
      class="card"
      draggable="true"
    >
      <img
        width="250"
        height="150"
        src="https://source.unsplash.com/category/buildings/250x150"
        draggable="false"
      />
      <div class="card-text">
        <h3>Some Title</h3>
        <span>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam...</span>
      </div>
    </div>
    <div
      class="card"
      draggable="true"
    >
      <img
        width="250"
        height="150"
        src="https://source.unsplash.com/collection/190727/250x150"
        draggable="false"
      />
      <div class="card-text">
        <h3>Some Title</h3>
        <span>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam...</span>
      </div>
    </div>
    <div
      class="card"
      draggable="true"
    >
      <img
        width="250"
        height="150"
        src="https://source.unsplash.com/user/erondu/likes/250x150"
        draggable="false"
      />
      <div class="card-text">
        <h3>Some Title</h3>
        <span>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam...</span>
      </div>
    </div>
    <div
      class="card"
      draggable="true"
    >
      <img
        width="250"
        height="150"
        src="https://source.unsplash.com/user/erondu/250x150"
        draggable="false"
      />
      <div class="card-text">
        <h3>Some Title</h3>
        <span>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam...</span>
      </div>
    </div>

    <!-- a card that is not draggable -->
    <div
      class="card"
      title="not draggable. sorry ;-)"
      draggable="false"
    >

      <div class="card-head">
        <span class="name">jet-plugin-classList</span>
        <!-- https://stackoverflow.com/questions/22932422/get-github-avatar-from-email-or-name -->
        <img
          class="author"
          width="50"
          height="50"
          title="Max Mustermann"
          src="https://github.com/github.png?size=50"
          draggable="false"
        />
      </div>

      <div class="card-text">
        <h3>ClassList</h3>
        <span>Plugin to maniplute the elements classList.</span>
      </div>
    </div>
  </div>

</template>

<script>
const dnd = (element, options) => {
  // find all dragable elements
  var draggableElements = element.querySelectorAll('[draggable=true]');
  var activeDragElement;
  var placeholderElement;
  var startElementRect;
  console.log("Drag'n'Drop Container: ", element, 'Draggable elements: ', draggableElements);

  // Function responsible for sorting
  const _onDragOver = function (event) {
    placeholderElement.style.width = startElementRect.width + 'px';
    placeholderElement.style.height = startElementRect.height + 'px';
    placeholderElement.style.top = startElementRect.top + 'px';
    placeholderElement.style.left = startElementRect.left + 'px';
    console.log('Placeholder: ', placeholderElement, 'startRect: ', startElementRect);

    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';

    var target = closest(event.target, 'card', 'playground');
    if (target && target !== activeDragElement) {
      var rect = target.getBoundingClientRect();
      var horizontal = event.clientY > startElementRect.top && event.clientY < startElementRect.bottom;
      var next = false;

      if (horizontal) {
        next = (event.clientX - rect.left) / (rect.right - rect.left) > 0.5;
      } else {
        next = !((event.clientY - rect.top) / (rect.bottom - rect.top) > 0.5);
      }

      console.log('onDragOver target classlist: ', target);

      // insert at new position
      element.insertBefore(activeDragElement, next && target.nextSibling || target);

      // update rect for insert poosition calculation
      startElementRect = activeDragElement.getBoundingClientRect();
    }
  };

  // handle drag event end
  const _onDragEnd = function (event) {
    event.preventDefault();

    placeholderElement.style.width = '0px';
    placeholderElement.style.height = '0px';
    placeholderElement.style.top = '0px';
    placeholderElement.style.left = '0px';

    activeDragElement.classList.remove('moving');
    element.removeEventListener('dragover', _onDragOver, false);
    element.removeEventListener('dragend', _onDragEnd, false);
  };

  element.addEventListener('dragstart', function (event) {
    // don't allow selection to be dragged if it is not draggable
    if (event.target.getAttribute('draggable') !== 'true') {
      event.preventDefault();
      return;
    }

    activeDragElement = event.target;
    startElementRect = activeDragElement.getBoundingClientRect();

    // Limiting the movement type
    event.dataTransfer.effectAllowed = 'move';

    // setData => Fuinktioniert im IE nicht bzw. nur bedingt
    // !!!! wird aber scheinbar im Firefox für die Vorschau benötigt
    // event.dataTransfer.setData('text/html', activeDragElement.innerHtml);
    event.dataTransfer.setData('text/uri-list', 'http://www.mozilla.org');

    // Subscribing to the events at dnd
    element.addEventListener('dragover', _onDragOver, false);
    element.addEventListener('dragend', _onDragEnd, false);

    activeDragElement.classList.add('moving');

    // import placeholder
    placeholderElement = element.querySelector('.tpl-placeholder');
  });
};

// active the drag'n'drop functionallity for the .playground element
dnd(document.querySelector('.playground'));

export default {

  // helper to find the closest parent by class with on optional stop class to stop searching
  closest (el, clazz, stopClazz) {
    if (el.classList.contains(stopClazz)) return null;

    while ((el = el.parentElement) &&
      !el.classList.contains(clazz) &&
      !el.classList.contains(stopClazz));

    return el.classList.contains(stopClazz) ? null : el;
  }

};
</script>

<style>
* {
  box-sizing: border-box;
}
template {
  display: none; /* IE support */
}

body {
  font-family: "Raleway", sans-serif;
  padding: 0;
  margin: 0;
}

.playground {
  background: #eee;
  padding: 4rem 4rem;
}

/** clear floating **/
.playground::after {
  clear: both;
  content: "";
  display: table;
}

.card {
  display: inline-block;
  float: left; /** optional, better alignment for multi-row use cases -> or use flexbox */
  background: #fff;
  width: 250px;
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.15), 0 0 4px 0 rgba(0, 0, 0, 0.2),
    0 12px 12px 0 rgba(0, 0, 0, 0.15);
  margin: 0.5rem 1rem;
  transition: box-shadow 0.2s ease-in-out;
}

.card[draggable="true"] {
  cursor: move;
}

.card[draggable="false"] {
  cursor: not-allowed;
}

/* Prevent the text contents of draggable elements from being selectable. Also from Elements which are explicit not draggable */
.playground {
  -moz-user-select: none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}

.card:hover {
  box-shadow: 0 0 18px 0 rgba(0, 0, 0, 0.1), 0 0 36px 0 rgba(0, 0, 0, 0.15),
    0 36px 36px 0 rgba(0, 0, 0, 0.2);
}

.card > img {
  padding: 0;
  margin: 0;
}
.card-text {
  padding: 0.75rem;
}
.card-text > h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  line-height: 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
}
.card-text > h3:hover {
  color: green;
}
.card-text > span {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1rem;
  font-weight: 200;
}

.card-placeholder {
  position: fixed;
  display: inline-block;
  background: #ddd;
}
.card.moving {
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0), 0 0 4px 0 rgba(0, 0, 0, 0),
    0 12px 12px 0 rgba(0, 0, 0, 0);
}

.card-head {
  background: #eee;
  padding: 2.5rem 1rem;
  text-align: center;
  font-family: Menlo, "Courier New";
  position: relative;
}

.author {
  position: absolute;
  display: inline-block;
  right: 1rem;
  bottom: -25px;
  border-radius: 50px;
}
</style>
