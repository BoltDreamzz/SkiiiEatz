document.addEventListener("DOMContentLoaded", function () {
  const viewportWidth = window.innerWidth;

  // Rider 1: left to right (faster)
  gsap.fromTo(".rider-1", 
    { x: -150, y: 0 },
    { x: viewportWidth + 150, duration: 3, repeat: -1, ease: "none" } // was 8
  );

  // Rider 2: right to left (faster)
  gsap.fromTo(".rider-2", 
    { x: viewportWidth + 150, y: 80 },
    { x: -150, duration: 6, repeat: -1, ease: "none" } // was 10
  );

  // Rider 3: diagonal (faster)
  gsap.fromTo(".rider-3",
    { x: -150, y: 200 },
    { x: viewportWidth + 150, y: -50, duration: 7, repeat: -1, ease: "none" } // was 12
  );

  // Optional bounce on hover
  document.querySelectorAll(".delivery-riders img").forEach(img => {
    img.addEventListener("mouseenter", () => {
      gsap.to(img, { scale: 1.1, duration: 0.3 });
    });
    img.addEventListener("mouseleave", () => {
      gsap.to(img, { scale: 1, duration: 0.3 });
    });
  });
});
