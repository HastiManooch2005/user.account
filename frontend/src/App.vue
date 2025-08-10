<template>
  <div class="user-form">
    <h1>user Form</h1>

    <form @submit.prevent="submitHandler">
      <div>
        <label>username:</label>
        <input type="text" placeholder="enter username" v-model="form.username" />
      </div>

      <div>
        <label>Full name:</label>
        <input type="text" placeholder="enter full name" v-model="form.fullname" />
      </div>

      <div>
        <label>Password:</label>
        <input type="password" placeholder="password" v-model="form.password" />
      </div>

      <div v-if="form.username && form.fullname && form.password">
        <button :disabled="loading">save</button>
      </div>
      <div v-else>
        <p>please fill all fields</p>
      </div>
    </form>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">{{ success }}</div>

    <h2>user list</h2>

    <div v-if="loading">Loading users...</div>
    <ul v-else>
      <li v-for="(u, index) in users" :key="u.id ?? index">
        {{ u.username }} - {{ u.fullname }}
        <button @click="deleteUser(index)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'



const form = ref({
  username: '',
  fullname: '',
  password: ''
})

const users = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get("http://127.0.0.1:8000/list/users")
    // انتظار داریم پاسخ: { users: [...] }
    users.value = res.data.users || []
  } catch (err) {
    console.error('Failed to fetch users:', err)
    error.value = 'خطا در گرفتن کاربران — بررسی کن سرور روشن باشه'
  } finally {
    loading.value = false
  }
}

async function submitHandler() {
  error.value = ''
  success.value = ''
  try {
    const payload = {
      username: form.value.username,
      fullname: form.value.fullname,
      password: form.value.password
    }
    const res = await axios.post('http://127.0.0.1:8000/register/user', payload)
    success.value = 'ثبت موفق'
    // اگر توی response توکن ارسال شد، ذخیره کن
    if (res.data.tokens) {
      localStorage.setItem('access', res.data.tokens.access)
      localStorage.setItem('refresh', res.data.tokens.refresh)
    }
    // تازه‌سازی لیست کاربران (یا اضافه کردن دستی)
    await fetchUsers()
    // و پاک کردن فرم
    form.value = { username: '', fullname: '', password: '' }
  } catch (err) {
    console.error('Register error:', err)
    if (err.response && err.response.data) {
      // نمایش خطاهای serializer
      error.value = JSON.stringify(err.response.data)
    } else {
      error.value = 'خطا در ثبت نام'
    }
  }
}

async function deleteUser(index) {
  const userId = users.value[index].id
  try {
    await axios.delete(`http://127.0.0.1:8000/delete/${userId}/`)

    users.value.splice(index, 1)
    success.value = 'کاربر حذف شد'
  } catch (err) {
    console.error('Delete error:', err)
    error.value = err.response?.data?.detail || 'خطا در حذف کاربر'
  }
}



onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
/* از CSS خودت استفاده کن — بدون تغییر */
.user-form{
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
h1,h2{
  text-align: center;
}
form div{
  margin-bottom: 15px;
}
label{
  display: block;
   margin-bottom: 5px;
   font-weight: bold;
}
input{
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button{
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled{
  background-color: #ccc;
}
ul{
  list-style: none;
  padding: 0;
}
li{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
li button{
  padding: 5px 10px;
   background-color: #e74c3c;
   color: white;
   border: none;
   border-radius: 4px;
   cursor: pointer;
}
li button:hover{
  background-color: #c0392b;
}
.error { color: red; margin-top: 10px; }
.success { color: green; margin-top: 10px; }
</style>
