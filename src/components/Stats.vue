<template>
  <section class="stats">
    <div class="stat-item animate-on-scroll">
      <h3>۱۰۰۰+</h3>
      <p>پروژه‌های سالانه</p>
    </div>
    <div class="stat-item animate-on-scroll">
      <h3>۹</h3>
      <p>نوع خدمات</p>
    </div>
    <div class="stat-item animate-on-scroll">
      <h3>۹۰+</h3>
      <p>کارمندان</p>
    </div>
    <div class="stat-item animate-on-scroll">
      <h3>۱۰۰+</h3>
      <p>مشتریان راضی</p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Stats'
}
</script>

<style scoped>
.stats {
  background: #00BFFF;
  color: white;
  padding: 25px 250px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  text-align: center;
  direction: rtl;
}

.stat-item {
  transition: transform 0.3s cubic-bezier(0.8, 0, 0.2, 1);
}

.stat-item:hover {
  transform: scale(1.05);
}

.stat-item h3 {
  font-size: 40px;
  font-weight: 900;
  color: white;
  margin-bottom: 8px;
}

.stat-item p {
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
}

@media (max-width: 1024px) {
  .stats {
    padding: 30px 30px;
    gap: 50px;
  }

  .stat-item h3 {
    font-size: 36px;
  }
}

@media (max-width: 768px) {
    .stats {
    display: none;
    grid-template-columns: repeat(2, 1fr);
    padding: 30px 20px;
    gap: 20px;
  }

  .stat-item h3 {
    font-size: 28px;
    margin-bottom: 8px;
  }

  .stat-item p {
    font-size: 12px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .stats {
    grid-template-columns: 1fr;
    padding: 20px 15px;
    gap: 15px;
  }

  .stat-item h3 {
    font-size: 24px;
  }

  .stat-item p {
    font-size: 11px;
    min-height: 44px;
  }
}
</style>
