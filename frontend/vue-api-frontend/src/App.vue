<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const responses = ref([]);
const loading = ref(true);
const error = ref(null);

// Fetch data from FastAPI
const fetchAPIResponses = async () => {
  try {
    loading.value = true;
    const { data } = await axios.get("http://127.0.0.1:8000/fetch-apis");
    console.log(data);
    responses.value = data;
  } catch (err) {
    error.value = "Failed to fetch data!";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchAPIResponses);
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-3xl font-bold text-center text-blue-600">Common Research API Fetcher</h1>
    
    <button
      @click="fetchAPIResponses"
      class="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700"
    >
      Refresh Data
    </button>

    <div v-if="loading" class="text-center mt-4">Loading...</div>
    <div v-if="error" class="text-red-500 text-center mt-4">{{ error }}</div>

    <div v-else class="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="(item, index) in responses"
        :key="index"
        class="bg-white shadow-md p-4 rounded"
      >
        <p class="text-gray-600 font-medium">📡 {{ item.url }}</p>

        <p v-if="item.response" class="text-green-500 mt-2 truncate">
          ✅ Success: {{ item.response.slice(0, 100) }}...
        </p>
        <p v-else class="text-red-500 mt-2">❌ Error: {{ item.error }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>