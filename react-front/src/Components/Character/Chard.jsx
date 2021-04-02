import Button from 'react-bootstrap/button';

const Chard = (props) => {
  const img = props.img;
  const name = props.name;
  const desc = props.desc;

  return (
    <div className="chard container">
      <img src={ img } alt="Pixel Portrait"/>
      <p className="chard title">{ name }</p>
      <p className="chard desc">{ desc }</p>
      <Button> More Info </Button>
    </div>
  )
}

export default Chard;
