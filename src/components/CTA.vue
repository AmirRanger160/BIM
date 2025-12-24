<template>
  <section class="cta">
    <div class="cta-item animate-on-scroll">
      <p style="color: rgba(255,255,255,0.8); font-size: 12px; text-transform: uppercase;">برنامه‌ریزی یک پروژه؟</p>
      <h2>ما را استخدام کنید</h2>
    </div>
    <div class="cta-item animate-on-scroll">
      <p style="color: rgba(255,255,255,0.8); font-size: 12px; text-transform: uppercase;">می‌خواهید به تیم ما بپیوندید؟</p>
      <h2>با ما کار کنید</h2>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CTA'
}
</script>

<style scoped>
.cta {
  background: #1abc9c;
  color: white;
  padding: 60px 50px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  text-align: center;
  direction: rtl;
  margin: 0 auto;
}

.cta-item {
  padding: 20px;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.cta-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-4px);
}

.cta-item h2 {
  font-size: 28px;
  font-weight: bold;
  margin-top: 10px;
}

.cta-item p {
  font-size: 14px;
  margin-top: 10px;
}

@media (max-width: 1024px) {
  .cta {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .cta {
    grid-template-columns: 1fr;
    padding: 30px 20px;
    gap: 20px;
  }

  .cta-item {
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 20px;
  }

  .cta-item h2 {
    font-size: 22px;
  }

  .cta-item p {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .cta {
    padding: 20px 15px;
    gap: 15px;
  }

  .cta-item {
    min-height: 80px;
    padding: 15px;
  }

  .cta-item h2 {
    font-size: 18px;
  }

  .cta-item p {
    font-size: 11px;
  }
}
</style>
