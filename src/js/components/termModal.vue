<template>
<div class="modal" :class="{ 'is-active': isActive }">
  <div class="modal-background" @click="closeModal"></div>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">利用規約</p>
      <button class="delete" aria-label="close" @click="closeModal"></button>
    </header>
    <section class="modal-card-body">
      <div class="content">
        <div>
          <h3>1. サイト運営者</h3>
          <p>
            当サイトは、<a href="https://twitter.com/shirakiya831">shirakiya</a>が運営しています。お問い合わせがある場合にはTwitterにてMentionあるいはDMでのご連絡をお願いします。
          </p>
        </div>
        <br />
        <div>
          <h3>2. サイト利用規約適用の範囲</h3>
          <p>
            本規約は、利用者による当サイトの利用全てに適用されます。利用者が当サイトを利用するには、本規約を遵守して頂くものとします。
          </p>
        </div>
        <br />
        <div>
          <h3>3. 提供するサービスの内容</h3>
          <p>
            当サイトは、<a href="https://arxiv.org/" target="_blank">arXiv.org</a>の一部コンテンツを<a href="https://cloud.google.com/translate/" target="_blank">Google Cloud Translation API</a>を用いて日本語に翻訳し、紹介するサイトです。
          </p>
        </div>
        <br />
        <div>
          <h3>4. 免責事項</h3>
          <p>
            <ol>
              <li>
                当サイトにコンテンツを掲載するにあたって、その内容、機能等について細心の注意を払っておりますが、コンテンツの内容が正確であるかどうか、最新のものであるかどうか、安全なものであるか等について保証をするものではなく、何らの責任を負うものではありません。また、事前に通知することなく当サイトに掲載した情報の訂正、修正、追加、中断、削除等をいつでも行うことができるものとします。<br />
                また、当サイト、またはコンテンツのご利用により、万一、ご利用者様に何らかの不都合や損害が発生したとしても、当方は何らの責任を負うものではありません。
              </li>
              <li>
                このサービスには、Google により提供される翻訳が含まれる場合があります。Google は、明示的か黙示的かを問わず、翻訳に関するすべての保証（精度、信頼性に関するあらゆる保証、および商品性、特定目的への適合性、第三者の権利の非侵害性に関するあらゆる黙示的保証を含みます）を放棄します。
              </li>
            </ol>
          </p>
        </div>
      </div>
    </section>
  </div>
</div>
</template>

<script>
export default {
  props: {
    isActive: Boolean,
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
  },
}
</script>

<style lang="scss" scoped>
</style>
