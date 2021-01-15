<template>
  <div id="form">
    <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="150px">
      <el-form-item label="设置抽奖机会接口" prop="setChance">
        <el-input v-model="formData.setChance" placeholder="请输入设置抽奖机会接口设置抽奖机会接口" clearable prefix-icon='el-icon-mobile' :style="{width: '100%'}"></el-input>
      </el-form-item>
      <el-form-item label="抽奖接口" prop="draw">
        <el-input v-model="formData.draw" placeholder="请输入抽奖接口" clearable
          prefix-icon='el-icon-mobile' :style="{width: '100%'}"></el-input>
      </el-form-item>
      <el-form-item label="奖池信息接口" prop="pool">
        <el-input v-model="formData.pool" placeholder="返回互斥策略，生效时间奖池信息接口"
          clearable prefix-icon='el-icon-mobile' :style="{width: '100%'}"></el-input>
      </el-form-item>
      <el-form-item label="奖品信息接口" prop="prize">
        <el-input v-model="formData.prize" placeholder="返回奖品信息借口"
          clearable prefix-icon='el-icon-mobile' :style="{width: '100%'}"></el-input>
      </el-form-item>
      <el-form-item size="large">
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
export default {
  name: 'Form',
  components: {},
  props: [],
  data() {
    return {
      formData: {
        setChance: '',
        draw: '',
        pool: '',
        field103: '',
      },
      rules: {
        setChance: [{
          required: true,
          message: '请输入设置抽奖机会接口',
          trigger: 'blur'
        }],
        draw: [{
          required: true,
          message: '请输入抽奖接口',
          trigger: 'blur'
        }],
        pool: [{
          required: true,
          trigger: 'blur'
        }],
        prize: [{
          required: true,
          trigger: 'blur'
        }],
      },
    }
  },
  computed: {},
  watch: {},
  created() {},
  mounted() {},
  methods: {
    submitForm() {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        console.log('submit!');
        console.log(this.formData.setChance);
          axios({
          method:'get',     
          url:"http://127.0.0.1:5000/test",
           params:{            
           },
          headers:{
             'Content-Type':'application/x-www-form-urlencoded',
          },
          
        })
          .then(response => {
            let status = response.data.code;
            if(status == 0){
              console.log('submit!');
              this.$message({
                message: '创建成功',
                type: 'success'
              })
            }
          })
      })
    },
    resetForm() {
      this.$refs['elForm'].resetFields()
    },
  }
}

</script>


<style>
.el-form-item{
    margin-bottom: 30px;
}
#form{
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}
</style>
