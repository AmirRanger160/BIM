<template>
  <section class="team">
    <h2 class="section-title animate-on-scroll">تیم ما</h2>
    <div class="team-grid">
      <div class="team-member animate-on-scroll" v-for="member in teamMembers" :key="member.id">
        <img 
          :src="member.image_url || 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 150 150%27%3E%3Crect fill=%27%23ddd%27 width=%27150%27 height=%27150%27/%3E%3C/svg%3E'" 
          :alt="member.name_fa || member.name_en"
          :title="`${member.name_fa || member.name_en} - ${member.position_fa || member.position_en}`"
        >
      </div>
    </div>
  </section>
</template>

<script>
import { teamService } from '../services/api';

export default {
  name: 'Team',
  data() {
    return {
      teamMembers: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchTeamMembers();
    this.$nextTick(() => {
      setTimeout(() => {
        const elements = this.$el.querySelectorAll('.animate-on-scroll');
        elements.forEach(el => el.classList.add('in-view'));
      }, 50);
    });
  },
  methods: {
    async fetchTeamMembers() {
      this.loading = true;
      this.error = null;
      try {
        const response = await teamService.getAll();
        this.teamMembers = response.data;
      } catch (err) {
        this.error = 'خطا در بارگذاری تیم';
        console.error('Error fetching team members:', err);
        this.teamMembers = [];
      } finally {
        this.loading = false;
      }
    }
  }
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
