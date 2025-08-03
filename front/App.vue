<template>
   <div class="user-form">
    <h1>user Form</h1>
    <form @submit.prevent="submitHandler">
      <div>
        <label>Name:</label>
        <input type="text" placeholder="enter your name" v-model="user.name">
      </div>

      <div>
        <label for="">Email:</label>
        <input type="email" placeholder="enter your email" v-model="user.email">
      </div>

      <div v-if="user.name && user.email">
        <button>save</button>
      </div>
      <div v-else>
        <p>please fill both</p>
      </div>
    </form>

    <h2>user list</h2>

    <ul>
      <li v-for="(user, index) in users" v-bind:key="index">{{ user.name }} - {{ user.email }}
        <button @click="deleteUser(index)">Delete</button>
      </li>
    </ul>
   </div>
</template>





<script setup>

import { ref } from 'vue';
const user = ref({name:"", email:""})
const users = ref([{name:'john', email:'john@email.com'}, {name:'ali', email:'ali@email.com'}])

function submitHandler(){
  if (user.value.name && user.value.email)
    {
        users.value.push(user.value)
        user.value = {name:"", email:""}
    }
}
function deleteUser(index){
  users.value.splice(index,1)
}
</script>










<style scoped>
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

</style>
