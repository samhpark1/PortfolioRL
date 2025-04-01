import Navbar from './components/Navbar.tsx';
import Hero from './components/Hero.tsx';
import Description from './components/Description.tsx';
import Pipeline from './components/Pipeline.tsx';
import Footer from './components/Footer.tsx';
import Model from './components/Model.tsx';
import StockViewer from './components/StockViewer.tsx';

function App() {

  return (
    <div>
      <Navbar />
      <Hero />
      <Description />
      <Pipeline />
      <Model />
      <Footer />

      {/* <Navbar />
      <StockViewer /> */}

    </div>
  )
}

export default App
