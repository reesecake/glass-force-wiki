import Flickity from 'react-flickity-component';
import Chard from './Chard';
import { useState, useEffect } from 'react';

import "./flickity.css";

const flickityOptions = {
  wrapAround: true,
  initialIndex: 1,

}

const Charousel = (props) => {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch('/api/pcs')
      .then(res => res.json())
      .then(data => {
        setData(data)
      })
    console.log(data);
  }, []);

  return (
    <Flickity
      elementType="div"
      options={flickityOptions}
    >
      { data && Object.keys(data).map((id) => (
        <Chard
          key={id}
          name={data[id]['name']}
          desc={data[id]['desc']}
          img={'assets/pixel_' + data[id]['name'].toLowerCase() + '.png'}
        />
      ))
      }
    </Flickity>
  )
}

export default Charousel;
