<template>
  <section class="team">
    <h2 class="section-title animate-on-scroll">تیم ما</h2>
    <div class="team-grid">
      <div class="team-member animate-on-scroll" v-for="n in 12" :key="n">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 150 150'%3E%3Crect fill='%23ddd' width='150' height='150'/%3E%3C/svg%3E" :alt="`تیم شماره ${n}`">
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Team'
}
</script>

<style scoped>
.team {
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.team > .team-grid {
  max-width: 1200px;
  width: 100%;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin-top: 50px;
  width: 100%;
}

.team-member {
  position: relative;
  overflow: hidden;
  border-radius: 5px;
  background: #f5f5f5;
}

.team-member img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 5px;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.team-member:hover img {
  transform: scale(1.08);
}

@media (max-width: 1024px) {
  .team {
    padding: 40px 30px;
  }
}

@media (max-width: 768px) {
  .team {
    padding: 30px 20px;
  }

  .team-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 30px;
  }

  .team-member {
    min-height: 120px;
  }
}

@media (max-width: 480px) {
  .team {
    padding: 20px 15px;
  }

  .team-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-top: 20px;
  }

  .team-member {
    min-height: 100px;
  }
}
</style>
