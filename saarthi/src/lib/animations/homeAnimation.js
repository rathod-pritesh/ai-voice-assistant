export function initHomeAnimation(canvas) {
  const ctx = canvas.getContext("2d");

  let particles = [];
  let animationFrameId;

  const config = {
    glowCount: 50,
    starCount: 40,
    nodeCount: 40,
    linkDistance: 140,
  };

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener("resize", resize);

  // --- Particle Classes ---
  class GlowOrb {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.radius = Math.random() * 2 + 1.5;
      this.dx = (Math.random() - 0.5) * 0.5;
      this.dy = (Math.random() - 0.5) * 0.5;
      this.opacity = Math.random() * 0.5 + 0.3;
    }
    update() {
      this.x += this.dx;
      this.y += this.dy;

      if (this.x < 0) this.x = canvas.width;
      if (this.x > canvas.width) this.x = 0;
      if (this.y < 0) this.y = canvas.height;
      if (this.y > canvas.height) this.y = 0;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(6, 182, 212, ${this.opacity})`; // cyan
      ctx.fill();
    }
  }

  class Star {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.radius = Math.random() * 1 + 0.7;
      this.dx = (Math.random() - 0.5) * 1.2;
      this.dy = (Math.random() - 0.5) * 1.2;
    }
    update() {
      this.x += this.dx;
      this.y += this.dy;

      if (this.x < 0) this.x = canvas.width;
      if (this.x > canvas.width) this.x = 0;
      if (this.y < 0) this.y = canvas.height;
      if (this.y > canvas.height) this.y = 0;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(255,255,255,0.9)";
      ctx.fill();
    }
  }

  // 3️⃣ Node particles (connect with lines)
  class Node {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.radius = Math.random() * 2 + 1;
      this.dx = (Math.random() - 0.5) * 0.4;
      this.dy = (Math.random() - 0.5) * 0.4;
    }
    update() {
      this.x += this.dx;
      this.y += this.dy;

      if (this.x < 0 || this.x > canvas.width) this.dx *= -1;
      if (this.y < 0 || this.y > canvas.height) this.dy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(6, 182, 212, 0.6)";
      ctx.fill();
    }
  }

  // --- Initialize All Particles ---
  function initParticles() {
    particles = [];

    for (let i = 0; i < config.glowCount; i++) particles.push(new GlowOrb());
    for (let i = 0; i < config.starCount; i++) particles.push(new Star());
    for (let i = 0; i < config.nodeCount; i++) particles.push(new Node());
  }

  initParticles();

  // --- Animation Loop ---
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update + Draw
    particles.forEach((p) => {
      p.update();
      p.draw();
    });

    // Draw lines between nodes only
    const nodes = particles.filter((p) => p instanceof Node);

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const n1 = nodes[i];
        const n2 = nodes[j];

        const dx = n1.x - n2.x;
        const dy = n1.y - n2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < config.linkDistance) {
          ctx.beginPath();
          ctx.moveTo(n1.x, n1.y);
          ctx.lineTo(n2.x, n2.y);
          ctx.strokeStyle = `rgba(6, 182, 212, ${0.3 * (1 - dist / config.linkDistance)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    animationFrameId = requestAnimationFrame(animate);
  }

  animate();

  return () => {
    cancelAnimationFrame(animationFrameId);
    window.removeEventListener("resize", resize);
  };
}
