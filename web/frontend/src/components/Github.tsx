import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function Github() {
  const textRef = useRef(null);

  const rawCode = `
class ActorCritic(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_size=64):
        super(ActorCritic, self).__init__()
        self.actor = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_dim),
            nn.Softmax(dim=-1)
        )
        self.critic = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, x):
        action_probs = self.actor(x)
        state_value = self.critic(x)
        return action_probs, state_value
  `;

  const codeLines = rawCode.split("\n");

  useEffect(() => {
    if (textRef.current) {
      // Clear the content first
      textRef.current.innerHTML = "";

      codeLines.forEach((line, index) => {
        const lineElement = document.createElement("span");
        lineElement.textContent = line;
        lineElement.style.display = "block";
        textRef.current.appendChild(lineElement);

        gsap.from(lineElement, {
          scrollTrigger: {
            trigger: textRef.current,
            start: "top 80%",
            toggleActions: "play none none reverse",
          },
          duration: 1,
          opacity: 0,
          y: 20,
          delay: index * 0.1,
          ease: "power2.out",
        });
      });
    }
  }, []);

  const linkHandler = () => {
    window.open("https://github.com/samhpark1/PortfolioRL", "_blank");
  }

  return (
        <div 
            className="m-10 p-5 hover:shadow-green-400 hover:shadow-lg hover:border-green-400 hover:border-2 rounded-xl min-w-1/2 max-w-1/2 text-[0.65rem] bg-gray-900 text-green-400 font-mono"
            onClick={linkHandler}
        >
            <pre
                ref={textRef}
                style={{
                whiteSpace: "pre-wrap",
                overflowX: "auto",
                lineHeight: "1.5",
                }}
            />
            <h1 className="flex justify-center pt-10 text-xl">Click to See our Github!</h1>
        </div>
    
  );
}

export default Github;
