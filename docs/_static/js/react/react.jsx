const useState = React.useState;
const MUI = window.MaterialUI;

function getComponentProps(node) {
  const attributeNames = node.getAttributeNames();
  const props = {};
  for (const attributeName of attributeNames) {
    if (attributeName.startsWith("data-")) {
      const propName = attributeName.slice(5);
      const decodedPropValue = decodeURIComponent(node.getAttribute(attributeName));
      // sphinx_state is a special prop value that should be parsed
      props[propName] = propName === "sphinx_state" ? JSON.parse(decodedPropValue) : decodedPropValue;
    }
  }
  return props;
}

function getPathToResource(sphinx_state, path) {
  return [...new Array(sphinx_state.page_nesting_level).fill(".."), path].join("/");
}

function mountComponent(querySelector, Component) {
  const containers = document.querySelectorAll(querySelector);
  for (const container of containers) {
    const props = getComponentProps(container);
    const root = ReactDOM.createRoot(container);
    root.render(<Component {...props} />);
  }
}

function LitTabs({ titles }) {
  // const [likeCount, setLikeCount] = useState(100500);
  return (
    <p>
      <p>{".. raw:: html"}</p>
      <p>{titles}</p>
    </p>
  );
}

mountComponent(".LitTabs", LitTabs);

// LikeButtonWithTitle Component

function LikeButtonWithTitle({ title, margin, padding }) {
  const [likeCount, setLikeCount] = useState(100500);
  return (
    <button onClick={() => setLikeCount(likeCount + 1)} style={{ margin, padding }}>
      Like {title} {likeCount}
    </button>
  );
}

mountComponent(".LikeButtonWithTitle", LikeButtonWithTitle);


// ReactGreeter component

function ReactGreeter() {
  const [name, setName] = useState("");
  const onSubmit = (event) => {
    event.preventDefault();
    alert(`Hello, ${name}!`);
  };
  return (
    <form onSubmit={onSubmit}>
      <input
        type="text"
        placeholder="Enter your name"
        required
        value={name}
        onChange={(event) => setName(event.target.value)}
      />
      <button type="submit" disabled={!name}>Submit</button>
    </form>
  );
}

mountComponent(".ReactGreeter", ReactGreeter);


// LikeButtonWithTitle Component
function AppCardDirective({ header_image, title, description, tags, width, preview, deploy, age }) {
  const [likeCount, setLikeCount] = useState(100500);
  return (
    <button onClick={() => setLikeCount(likeCount + 1)}>
      Age {age}
    </button>
  );
}

mountComponent(".AppCardDirective", AppCardDirective);
