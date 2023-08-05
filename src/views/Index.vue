<template>
  <el-container>
    <el-header>
      <el-menu
        default-active="1"
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="1">Stable Diffusion Playground</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <el-row :gutter="20" style="text-align: left">
        <el-col :sm="10" :xs="24">
          <el-form
            ref="playground"
            :model="form"
            label-width="80px"
            label-position="top"
            :rules="rules"
          >
            <el-form-item label="Models" prop="lora">
              <el-row class="loras" type="flex" justify="start">
                <el-radio-group v-model="form.lora">
                  <el-radio
                    border
                    :label="index"
                    v-for="(lora, index) in loras"
                    :key="lora"
                  >
                    <el-image
                      style="width: 80px; height: 120px"
                      :src="lora"
                      fit="fit"
                    ></el-image>
                  </el-radio>
                </el-radio-group>
              </el-row>
            </el-form-item>

            <el-form-item label="Prompt" prop="prompt">
              <el-input
                type="textarea"
                placeholder="Please input the prompt"
                rows="12"
                v-model="form.prompt"
              >
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="btnLoading"
                @click="onSubmit"
                v-if="credential"
                >GENERATE NOW</el-button
              >
              <div id="signin_button" v-else></div>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :sm="14" :xs="24">
          <el-empty
            :image-size="200"
            description="描述文字"
            v-if="!output"
          ></el-empty>
          <div style="text-align: left" v-else>
            <label
              class="el-form-item__label"
              style="
                display: block;
                float: none;
                text-align: left;
                margin-bottom: 10px;
              "
              >Gallery</label
            >
            <el-row class="output" type="flex" justify="start">
              <div v-for="(item, index) in output" :key="index">
                <el-image
                  style="width: 290px; height: 435px"
                  :src="item.image"
                  v-if="item.image"
                ></el-image>
                <div class="job" v-else>
                  <div style="width: 100%" v-loading="true"></div>
                  <h5>There are currently many people</h5>
                  <p>You are currently in {{ item.order + 1 }} place</p>
                  <p>
                    Estimated wait time is still
                    {{ (item.order + 1) * 15 }} seconds
                  </p>
                  <button>Refresh</button>
                </div>
              </div>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      btnLoading: false,
      output: [
        {
          image:
            "https://ik.imagekit.io/gptfriend/default-image.jpg?updatedAt=1684906019377",
        },
      ],
      loras: [
        "https://ik.imagekit.io/gptfriend/default-image.jpg?updatedAt=1684906019377",
        "image.daaka.cn/stablediffusion/1680512954_8382100962.png",
        "image.daaka.cn/stablediffusion/1680512954_8382100963.png",
        "image.daaka.cn/stablediffusion/1680512954_8382100964.png",
        "image.daaka.cn/stablediffusion/1680512954_8382100965.png",
        "image.daaka.cn/stablediffusion/1680512954_8382100969.png",
      ],
      form: {
        prompt: null,
        lora: 0,
      },
      rules: {
        prompt: [
          { required: true, message: "请填写活动形式", trigger: "blur" },
        ],
      },
      credential: localStorage.getItem("credential"),
    }
  },
  mounted() {
    if (!this.credential) {
      this.googleAuth()
      return
    }

    this.getJobs()
    this.getJobsByJobID()
    
  },
  methods: {
    googleAuth() {
      let googleScript = document.createElement("script")
      googleScript.src = "https://accounts.google.com/gsi/client"
      document.head.appendChild(googleScript)

      window.addEventListener("load", () => {
        window.google.accounts.id.initialize({
          client_id:
            "1029286495108-3107mjncjooi9mta6pngt74rqos3811l.apps.googleusercontent.com",
          callback: this.handleCredentialResponse,
        })
        window.google.accounts.id.renderButton(
          document.getElementById("signin_button"),
          {
            theme: "outline",
            size: "large",
            logo_alignment: "left",
            itp_support: "true",
            text: "signin_with",
          }
        )
      })
    },
    onSubmit() {
      this.$refs["playground"].validate((valid) => {
        if (valid && this.credential) {
          this.btnLoading = true
          this.$http
            .post("/generate", {
              lora: this.form.lora,
              prompt: this.form.prompt,
            })
            .then((resp) => {
              this.output.push(resp)
              this.btnLoading = false
            })
        } else {
          console.log("error submit!!")
          return false
        }
      })
    },
    getJobs() {
      this.$http.post("/jobs").then((resp) => {
        console.log("resp", resp)
        this.output = resp["jobs"]
      })
    },

    getJobsByJobID() {
      this.$http
        .post("/job", {
          job_id: ["RMvGdSsOzvyFe59lRVKl", "RtR2VPtInNnnGvVGguYH"],
        })
        .then((resp) => {
          if (resp["jobs"]) {
            this.output.forEach((item, index) => {
              const v = resp["jobs"].filter((k) => {
                return k["job_id"] === item["job_id"]
              })
              console.log("v", v)
              if (v.length > 0) {
                this.output[index] = v[0]
              }
            })
            console.log(11212312, this.output)
          }
        })
    },

    handleCredentialResponse(resp) {
      this.loginWithServer(resp.credential)
    },
    loginWithServer(token) {
      this.$http.post("/user", { token: token }).then((resp) => {
        console.log(resp)
        localStorage.setItem("credential", resp)
        this.credential = resp
      })
    },
  },
}
</script>

<style>
#signin_button {
  width: 150px;
}
.el-header {
  padding: 0px !important;
}
.el-radio__label {
  padding-left: 0px !important;
}
.el-radio__inner {
  display: none !important;
}
.el-radio.is-bordered {
  height: auto !important;
  padding: 0px !important;
}

.el-radio.is-bordered + .el-radio.is-bordered {
  margin-left: 0px !important;
}
.el-image {
  border-radius: 4px;
}

.loras {
  overflow-x: auto;
  white-space: nowrap;
}

.loras .el-image {
  flex: 0 0 auto;
}

.loras .el-radio {
  margin-right: 8px !important;
}

.output {
  overflow-x: auto;
  white-space: nowrap;
  border: 1px solid #dcdfe6;
  padding: 12px 12px 5px 12px;
}

.output .el-image {
  flex: 0 0 auto;
  margin-right: 12px;
}

.job {
  width: 290px;
  height: 435px;
  background-color: red;
  flex: 0 0 auto;
  margin-right: 12px;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
</style>
