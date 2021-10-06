With portal you can render child node to html body

```jsx
<Portal>
  <div style={{height: '50px', color: 'green', marginLeft: '250px'}}>HELLO HELLO HELLO HELLO HELLO</div>
</Portal>
```


Or you can render the child node to any other node that has an ID

```jsx
<div id="portal-root-2" />
<div>
  Should be rendered below this
  <Portal to="portal-root-2">
    <div>But it is above</div>
  </Portal>
</div>
```
