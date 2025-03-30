import {useGSAP} from '@gsap/react';
import gsap from 'gsap';

function Hero() {
  useGSAP(() => {
    gsap.fromTo('.intro', {
        y: 50,
        opacity: 0,
    },
    {
        opacity: 1,
        y:0,
        delay: 1,
        stagger: .5
    })

    gsap.to('.scroll', {
        y: 25,
        delay: 3,
        repeat: -1,
        yoyo: true,
        ease: 'power1.inOut',
        duration: 1,
    })
  }, [])


    return (
      <div className="flex flex-col justify-between h-screen bg-linear-to-br from-black to-purple-950 z-0 px-10 pt-20 pb-10">
        <section className="intro flex flex-col">
          <h1 className="text-8xl font-bold text-gray-200">PortfolioRL</h1>
          <p className="text-xl text-gray-300 max-w-sm">A Deep Reinforcement Learning Project for Portfolio Optimization</p>
        </section>
        <section className='flex justify-center'>
          <div className='rounded-full max-w-5 h-10 ring-gray-300 ring-2'>
              <div className='scroll h-2 w-2 rounded-full bg-white m-1'/>
          </div>
        </section>
      </div>
    )
  }
  
  export default Hero
  