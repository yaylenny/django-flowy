<script>
  import FlowItem from "./Flow.vue";

  export default{
    name: 'flow-item',
    props: {
      id: Number,
      text: String,
      fid: Number,
      index: Number,
      complete: Boolean,
      children: Array,
      parent: Number,
      expanded: Boolean,
      hovered: Boolean,
      items: Array // sent only at the top ( from App )
    },
    data(){
      return {
        rawText: this.text || '',
        menuTimer: 0,
        menuVisible: false,
        cleared: false, //set once when backspace is used and no rawText
      };
    },
    components:{ FlowItem },
    computed:{
      active(){
        return this.id && ( this.id==this.$store.state.active );
      }
    },
    methods:{
      focusBullet(){

      },
      onBackSpace( e, id ){
        if( this.rawText ) return;
        if( this.cleared ){
          this.$emit('backout', e, id || this.id );
        }
        else this.cleared=true;
      },
      onBlur( e, id ){
        this.$emit('blur', e, id || this.id )
      },
      onBullet( e, id ){
        this.$emit('bullet', e, id || this.id )
      },
      onBulletHover( e ){
        // console.log( 'bullet hover enter')
        clearTimeout( this.menuTimer );
        this.menuTimer=setTimeout(()=>{
          clearTimeout( this.menuTimer );
          this.$emit('menu', e, this.id );
        }, 250 );
      },
      onChange( id, text ){
        this.$emit('change', id, text )
      },
      onClick( e, id ){
        this.$emit('click', e, id || this.id )
      },
      onFocus( e, id ){
        this.$emit('focus', e, id || this.id )
      },
      onEnter( e, id ){
        this.$emit('enter', e, id || this.id )
      },
      onKeyDown( e, id ){
        this.$emit('keydown', e, id || this.id )
      },
      onMenu( e, id ){
        this.$emit('menu', e, id || this.id )
      },
      onToggle( e, id ){
        this.$emit('toggle', e, id || this.id )
      },
      onTab( e, id ){
        this.$emit('tab', e, id || this.id )
      }
    },
    created(){},
    watch:{
      active( b ){
        if( b ){
          this.$refs.input.focus();
        }
      },
      rawText( text ){
        this.$emit('change', this.id, text )
      },
      hovered( b ){
        if( b ){
          this.menuVisible=true;

        }
        else{
          this.menuVisible=false;
        }
      }
    }
  }
</script>
<template lang="pug">
  .flow-item( :class="{'item-active': active }" )
    .item-body( @click="onClick")
      .item-spacer: .item-toggle( @click="$emit('toggle', $event, id )" v-if="(children && children.length)")
        span.toggle
          i.fa.fa-plus( v-if="expanded" )
          i.fa.fa-minus( v-else )
      .item-spacer: .item-bullet( @click="onBullet" @mouseenter="onBulletHover")
        span.bullet
      .item-text
        input( type="text" v-model="rawText"
          ref="input"
          @blur="$emit('blur', $event, id )"
          @focus="$emit('focus', $event, id )"
          @keydown.enter.stop="$emit('enter', $event, id )"
          @keydown.tab.prevent.stop="$emit('tab', $event, id )"
          @keydown.backspace="onBackSpace"
          @keydown="$emit('keydown', $event, id )")
      ul.item-menu( v-show="menuVisible")
        li: a( @click="" ) Expand
    .item-children( v-show="expanded")
      template( v-if="(children && children.length)")
        flow-item( v-for="item in children"
          :text="item.text"
          :key="item.id"
          :id="item.id"
          :parent="item.parent"
          :children="item.children"
          @change="onChange"
          @toggle="onToggle( $event, item.id )"
          @menu="onMenu( $event, item.id )"
          @keydown="onKeyDown( $event, item.id )"
          @focus="onFocus( $event, item.id )"
          @blur="onBlur( $event, item.id )"
          @tab="onTab( $event, item.id )"
          @bullet="onBullet( $event, item.id )"
          @enter="onEnter( $event, item.id )")
</template>
